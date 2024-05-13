from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Order:
    def __init__(self,data):
        self.id=data['id']
        self.vehicle_type=data['vehicle_type']
        self.years=data['years']
        self.marke=data['marke']
        self.model=data['model']
        self.Img=data['Img']
        self.price=data['price']
        self.description=data['description']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']
        self.owner = user_model.User.get_by_id({'id':self.user_id})



    @classmethod
    def save_order(cls, data): #!CREATE
       query = "INSERT INTO orders (user_id, vehicle_type, model, Img, marke, years, price, description) VALUES (%(user_id)s, %(vehicle_type)s, %(model)s, %(Img)s, %(marke)s, %(years)s, %(price)s, %(description)s);"
       return connectToMySQL(DATABASE).query_db(query, data)
    
 
   
 #get all orders
    @classmethod  #read 
    def get_orders(cls): #!READ
        query="SELECT * FROM orders;" 
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        orders=[]
        for row in results:
            orders.append(cls(row))
        return orders
    
     
    
    #get one order by id
    @classmethod
    def get_by_id_order(cls,data): #!READ
        query="SELECT * FROM orders WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    


       
    # Update the update_order method
    @classmethod
    def update_order(cls, data):
        query = """
            UPDATE orders 
            SET vehicle_type=%(vehicle_type)s,
                years=%(years)s,  
                marke=%(marke)s,
                model=%(model)s,
                Img=%(Img)s,
                price=%(price)s
            WHERE id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
        

 
    
    @classmethod
    def delete_order(cls,data): #!DELETE
        query="DELETE FROM orders WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
  



    #get one order by id
    @classmethod
    def get_by_id_order(cls,data): #!READ
        query="SELECT * FROM orders WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
 


    #validate order 
    @staticmethod #!VALIDATION
    def validate_order(data): 
        is_valid = True

       
        
        return is_valid
    
