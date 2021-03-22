'''
Created on 16-Mar-2021

@author: Admin
'''
from flask import Flask, render_template, request

from dbConnection import dbConnect





app = Flask (__name__,template_folder='template')



@app.route("/",methods=["GET", "POST"])
def usermanagement():
    #data=getmemberinfo()
    if request.method == "POST":
        
        #print("post")
        data=getmemberinfo()
        
        #print(data)
        return render_template("home.html",data=data)
        #return "dsfdg"
    elif request.method=="GET":
        print("get")
        db = dbConnect()
        data=getmemberinfo()
        cur = db.cursor(prepared=True)
        flag=request.args.get("flag")
        if flag=="delete":
            #print("change")
            user_role_id=request.args.get("user_role_id")
            cur.execute("delete from `user_roles` where `user_role_id` ="+user_role_id)
            db.commit() 
            #print(cur.rowcount, "record(s) deleted")
            #print("Record Deleted successfully ")  
            
            data=getmemberinfo()
            db.commit() 
            return render_template("home.html",data=data)
        if flag=="edit":
            #print("edit")
            user_role_id=int(request.args.get("user_role_id"))
            #print(type(user_role_id))
            #print("id is here",user_role_id)
          
            data1=getmemberinfobyid(user_role_id)
            roles_data=getrolesinfo()
            #db.commit() 
            return render_template("update_user.html",data1=data1,roles_data=roles_data)
        return render_template("home.html",data=data)







@app.route("/adduser",methods=["GET","POST"])
def adduser():
    #print("add user")
    if request.method=="POST":
        #print("post from add user")
        db = dbConnect()
        cur = db.cursor(prepared=True)
        role = request.form.getlist('role')
        #print(role)
        first_name=request.form["firstname"]
        last_name=request.form["lastname"]
        user_name=request.form["username"]
        description=request.form["description"]
        #print(first_name,last_name,user_name,description)
        insert_user="""insert into user (`first_name`,`last_name`,`user_name`,`description`) values(%s,%s,%s,%s) """
        
        val = (first_name, last_name, user_name,description)
        cur.execute(insert_user,val)
        
        db.commit() 
        
        
        #return res
        if cur.rowcount>0:
            lastid=cur.lastrowid
            #print("data inserted",lastid,"",cur.lastrowid)
            role = request.form.getlist('role')
            #print(role)
            insert_user_role="""insert into user_roles (`role_id`,`user_id`) values(%s,%s); """
            val_user_role = [(int(val), lastid) for val in role] 
            #print("user roles",val_user_role)
            db = dbConnect()
            cur = db.cursor(prepared=True)
            cur.executemany(insert_user_role,val_user_role)
            if cur.rowcount>0:
                lastid_roles=cur.lastrowid
                #print("data inserted",lastid_roles)
            
            db.commit() 
            cur.close()
            db.close()
        
        else:
            #print("not installed")
            roles_data=getrolesinfo()
        
            return render_template("add_user.html",roles_data=roles_data)  
        
        
        roles_data=getrolesinfo()
        
        return render_template("add_user.html",roles_data=roles_data)  

    elif request.method=="GET":
        #print("get from add user")
 
        roles_data=getrolesinfo()

        return render_template("add_user.html",roles_data=roles_data)  



@app.route("/updateuser",methods=["GET","POST"])
def updateuser():
    #print("add user")
    if request.method=="POST":
        #print("post from add user")
        db = dbConnect()
        cur = db.cursor(prepared=True)
        role = request.form.getlist('role')
        #print(role)
    
        user_roles_id=request.form["user_roles_id"]
        description=request.form["description"]
        user_id=request.form["user_id"]
        
        #print(description)
        update_user="""update protegrity.user set description=%s where user.user_id=%s"""
        
        val = (description,user_id)
        cur.execute(update_user,val)
        db.commit()
        cur.close()
        db.close()
        if cur.rowcount>0:
        
            update_user_role="""update protegrity.user_roles set role_id=%s where user_roles.user_role_id=%s and user_roles.user_id=%s """
            val_user_role = [(int(val), user_roles_id,user_id) for val in role] 
            #print("user roles",val_user_role)
            db = dbConnect()
            cur = db.cursor(prepared=True)
            cur.executemany(update_user_role,val_user_role)
            if cur.rowcount>0:
                
                print("data updated")
            
            db.commit() 
            cur.close()
            db.close()


            data1=getmemberinfobyid(user_roles_id)
            roles_data=getrolesinfo()
            #db.commit() 
            return render_template("update_user.html",data1=data1,roles_data=roles_data)
        else:
            data=getmemberinfo() 
            return render_template("home.html",data=data)
        
        
         



def getrolesinfo():
    #print("from roles info")
    db = dbConnect()
    cur = db.cursor(prepared=True)
    cur.execute( """select * from roles ;"""  )
    res = cur.fetchall()

    db.commit() 
    cur.close()
    db.close()
     
    #print(res)
    return res



def getmemberinfo():
    db = dbConnect()
    cur = db.cursor(prepared=True)
    cur.execute( """select user.user_name, roles.role_name, user_roles.user_role_id
    from user,roles,user_roles 
    where roles.role_id=user_roles.role_id 
    and  user.user_id=user_roles.user_id order by user_role_id desc;"""  )
    res = cur.fetchall()
    #print(res)
    #db.commit() 
    #return render_template("home.html")


    db.commit() 
    cur.close()
    db.close()
    return res



def getmemberinfobyid(user_role_id):

    db = dbConnect()
    cur = db.cursor(prepared=True)
    getbyid="select user.first_name,user.last_name, user.user_name, user_roles.user_role_id,user.user_id  from user,user_roles where user.user_id=user_roles.user_id and user_roles.user_role_id=%s"
     
    id1=(user_role_id,)
    #print("id is here",id1)
    cur.execute(getbyid,id1)
    
    res = cur.fetchall()
    #print(res)
    #db.commit() 
    #return render_template("home.html")


    db.commit() 
    cur.close()
    db.close()
    return res
    
    



if __name__ == "__main__":

    app.secret_key = 'some secret key'
    #app.run(host='127.0.0.1', port=5000)
    app.run(debug=True) #if you want to change the port and host just try this code :-   app.run(host='127.0.0.1', port=5002)
    #app.config['TESTING'] = False