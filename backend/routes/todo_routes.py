from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from flask_mail import Message  # ✅ new import
from extensions import mongo, mail  # ✅ import mail

# Blueprint with prefix
todo_bp = Blueprint("todo", __name__, url_prefix="/api/todos")

# ✅ GET all todos for logged-in user
@todo_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_todos():
    user = get_jwt_identity()
    todos = mongo.db.todos.find({"user": user})
    output = []
    for t in todos:
        output.append({
            "_id": str(t["_id"]),
            "text": t.get("text", ""),
            "completed": t.get("completed", False)
        })
    return jsonify(output), 200

# ✅ POST a new todo and send email
@todo_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_todo():
    user = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("text"):
        return jsonify({"error": "Text is required"}), 400

    todo = {
        "text": data["text"],
        "completed": False,
        "user": user
    }

    inserted = mongo.db.todos.insert_one(todo)
    todo["_id"] = str(inserted.inserted_id)

    # ✅ Send email notification
    try:
        msg = Message(
            subject="🆕 New Todo Created",
            recipients=[user],
            body=f"Hello,\n\nA new todo was just created:\n\n📌 {todo['text']}\n\nThank you for using the Todo App!"
        )
        mail.send(msg)
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")

    return jsonify(todo), 201

# ✅ PUT (update: toggle or edit)
@todo_bp.route("/<id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_todo(id):
    user = get_jwt_identity()
    data = request.get_json()

    update_data = {}
    if "completed" in data:
        update_data["completed"] = data["completed"]
    if "text" in data:
        update_data["text"] = data["text"]

    if not update_data:
        return jsonify({"error": "Nothing to update"}), 400

    result = mongo.db.todos.update_one(
        {"_id": ObjectId(id), "user": user},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Todo not found"}), 404

    return jsonify({"message": "Todo updated"}), 200

# ✅ DELETE a todo
@todo_bp.route("/<id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_todo(id):
    user = get_jwt_identity()

    result = mongo.db.todos.delete_one({"_id": ObjectId(id), "user": user})
    if result.deleted_count == 0:
        return jsonify({"error": "Todo not found"}), 404

    return jsonify({"message": "Todo deleted"}), 200
