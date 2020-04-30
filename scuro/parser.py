













def _apply_vars(self):
    for key in request_data:
        if key[-1]=="@":
            k = request_data[key]
            v = vars.get(k)
            if v:
                rdict[key[:-1]] = v

def _ref_get(path,context=None):
    if context==None:
        context = {}
    if path[0]=="/":
        #relative path
        c = context
        for i in path.split("/"):
            if i:
                if isinstance(c,dict):
                    c = c.get(i)
                elif isinstance(c,list):
                    try:
                        c = c[int(i)]
                    except Exception as e:
                        raise ValueError("bad path item '%s' in path '%s', error: %s"%(i,path,e))
                else:
                    raise ValueError("cannot get '%s' from '%s'"%(i,c))
        return c
    else:
        #absolute path
        c = rdict
        for i in path.split("/"):
            if i:
                if isinstance(c,dict):
                    c = c.get(i)
                elif isinstance(c,list):
                    try:
                        c = c[int(i)]
                    except Exception as e:
                        raise ValueError("bad path item '%s' in path '%s', error: %s"%(i,path,e))
                else:
                    raise ValueError("bad path item '%s' in path '%s'"%(i,path))
        return c

def get(request_data):
    try:
        for key in request_data:
            if key[-1]=="@":
                #vars need to be applied later
                pass
            elif key[-2:]=="[]":
                rsp = _get_array(key)
            else:
                rsp = _get_one(key)
            if rsp: return rsp
        _apply_vars()
    except ValueError as e:
        return json({"code":400,"msg":str(e)})
    except Exception as e:
        err = "exception when handling 'apijson get': %s"%(e)
        #log.error(err)
        traceback.print_exc()
        return json({"code":400,"msg":"get exception when handling 'apijson get',please check server side log"})
    return json(rdict)

def _get_one(key):
    model_name = key
    params = request_data[key]
    params_role = params.get("@role")

    try:
        model = getattr(models, model_name)
        model_setting = settings.APIJSON_MODELS.get(model_name,{})
    except ModelNotFound as e:
        log.error("try to find model '%s' but not found: '%s'"%(model_name,e))
        return json({"code":400,"msg":"model '%s' not found"%(model_name)})
    model_column_set = None
    q = model.all()

    GET = model_setting.get("GET")
    if not GET:
        return json({"code":400,"msg":"'%s' not accessible"%(model_name)})

    roles = GET.get("roles")
    permission_check_ok = False
    if not params_role:
        if hasattr(request,"user") and request.user:
            params_role = "LOGIN"
        else:
            params_role = "UNKNOWN"
    elif params_role != "UNKNOWN":
        if not (hasattr(request,"user") and request.user):
            return json({"code":400,"msg":"no login user for role '%s'"%(params_role)})
    if params_role not in roles:
        return json({"code":400,"msg":"'%s' not accessible by role '%s'"%(model_name,params_role)})
    if params_role == "UNKNOWN":
        permission_check_ok = True
    elif functions.has_role(request.user,params_role):
        permission_check_ok = True
    else:
        return json({"code":400,"msg":"user doesn't has role '%s'"%(params_role)})
    if not permission_check_ok:
        return json({"code":400,"msg":"no permission"})

    if params_role=="OWNER":
        owner_filtered,q = _filter_owner(model,model_setting,q)
        if not owner_filtered:
            return  json({"code":400,"msg":"'%s' cannot filter with owner"%(model_name)})

    params = request_data[key]
    if isinstance(params,dict):
        #update reference,example: {"id@": "moment/user_id"} -> {"id": 2}
        ref_fields = []
        refs = {}
        for n in params:
            if n[-1]=="@":
                ref_fields.append(n)
                col_name = n[:-1]
                path = params[n]
                refs[col_name] = _ref_get(path,context=rdict)
        for i in ref_fields:
            del params[i]
        params.update(refs)
        
        for n in params:
            if n[0]=="@":
                if n=="@column":
                    model_column_set = set(params[n].split(","))
            elif hasattr(model,n):
                q = q.filter(getattr(model.c,n)==params[n])
            else:
                return json({"code":400,"msg":"'%s' have no attribute '%s'"%(model_name,n)})
    o = q.one()
    if o:
        o = o.to_dict()
        secret_fields = model_setting.get("secret_fields")
        if secret_fields:
            for k in secret_fields:
                del o[k]
        if model_column_set:
            keys = list(o.keys())
            for k in keys:
                if k not in model_column_set:
                    del o[k]
    rdict[key] = o

def _get_array(key):
    params = request_data[key]

    names = [n for n in params if n[0]!='@']
    if names:
        #main model
        n = names[0]
        mquery = ApiJsonModelQuery(n,params[n],key)
        mquery.query_array()
        #additional model
        for n in names[1:]:
            mquery = ApiJsonModelQuery(n,params[n],key)
            mquery.associated_query_array()
