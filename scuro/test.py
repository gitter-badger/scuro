from parser import get



request_data = {
  "[]":{                             
        "page":0,                        
        "count":2,
        "Moment":{                       
        "content$":"%a%"               
        },
        "User":{
        "id@":"/Moment/userId",      
        "@column":"id,name,head"      
        },
        "Comment[]":{                    
        "count":2,
        "Comment":{
            "momentId@":"[]/Moment/id"   
        }
        }
  }
}
