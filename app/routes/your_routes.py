from flask import Blueprint, jsonify, request
from app.models.your_model import YourModel
from app import db

your_bp = Blueprint('your', __name__)

# Get all items
@your_bp.route('/api/items', methods=['GET'])
def get_all_items():
    items = YourModel.query.all()
    return jsonify([item.to_dict() for item in items])

# Get single item
@your_bp.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = YourModel.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item.to_dict())

# Create new item
@your_bp.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate required fields
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_item = YourModel(
        title=data['title'],
        description=data.get('description', '')
    )
    
    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update item
@your_bp.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = YourModel.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        if 'title' in data:
            item.title = data['title']
        if 'description' in data:
            item.description = data['description']
        
        db.session.commit()
        return jsonify(item.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete item
@your_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = YourModel.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 