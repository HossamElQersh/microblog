from app.api import bp

@bp.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

@bp.route('/users/', methods=['GET'])
def get_users():
    pass

@bp.route('/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass

@bp.route('/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass



@bp.route('/users', methods=['POST'])
def create_user():
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass