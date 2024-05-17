from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.vehicle_type = data['vehicle_type']
        self.years = data['years']
        self.marke = data['marke']
        self.model = data['model']
        self.Img = data['Img']
        self.price = data['price']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = user_model.User.get_by_id({'id': self.user_id})
        self.likes_count = data.get('likes_count', 0)

    @classmethod
    def save_order(cls, data):
        query = """
            INSERT INTO orders (user_id, vehicle_type, model, Img, marke, years, price, description) 
            VALUES (%(user_id)s, %(vehicle_type)s, %(model)s, %(Img)s, %(marke)s, %(years)s, %(price)s, %(description)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_with_likes(cls):
        query = """
            SELECT o.*, COUNT(ulv.users_id) AS likes_count
            FROM orders o
            LEFT JOIN users_liked_vehicle ulv ON o.id = ulv.orders_id
            GROUP BY o.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        orders = []
        for result in results:
            order = cls(result)
            order.likes_count = result['likes_count']
            orders.append(order)
        return orders

    @classmethod
    def get_by_id_order(cls, data):
        query = "SELECT * FROM orders WHERE id=%(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update_order(cls, data):
        query = """
            UPDATE orders 
            SET vehicle_type=%(vehicle_type)s,
                years=%(years)s,  
                marke=%(marke)s,
                model=%(model)s,
                Img=%(Img)s,
                price=%(price)s,
                description=%(description)s
            WHERE id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_order(cls, order_id):
        query_likes = "DELETE FROM users_liked_vehicle WHERE orders_id = %(order_id)s;"
        connectToMySQL(DATABASE).query_db(query_likes, {'order_id': order_id})

        query_order = "DELETE FROM orders WHERE id = %(order_id)s;"
        connectToMySQL(DATABASE).query_db(query_order, {'order_id': order_id})

    @classmethod 
    def add_user_like(cls, data):
        query = "INSERT INTO users_liked_vehicle (users_id, orders_id) VALUES (%(users_id)s, %(orders_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def remove_user_like(cls, data):
        query = "DELETE FROM users_liked_vehicle WHERE users_id = %(users_id)s AND orders_id = %(orders_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_likes_count(cls, order_id):
        query = "SELECT COUNT(*) AS likes_count FROM users_liked_vehicle WHERE orders_id = %(order_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, {'order_id': order_id})
        return result[0]['likes_count']

    @staticmethod
    def validate_order(data):
        is_valid = True
        # Add your validation logic here
        return is_valid





    @classmethod
    def user_has_liked(cls, data):
        query = "SELECT * FROM users_liked_vehicle WHERE users_id = %(users_id)s AND orders_id = %(orders_id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return len(result) > 0
    


    