from flask import render_template, request, redirect, flash, session

from flask_app import app

from flask_app.models import message

@app.route('/messages/delete/<int:id>')
def delete_message(id):
    id_to_delete = message.Message.get_message_recipient({"id":id})
    if id_to_delete != session["user_id"]:
      if 'num_attempt' not in session:
        session["num_attempt"] = 1
        session["last_attempt"] = id
        session["ip_address"] = request.remote_addr
      else:
        session["num_attempt"] += 1
        session["last_attempt"] = id
        session["ip_address"] = request.remote_addr
      return redirect("/error_attempt")
    message.Message.delete_message({"id":id})
    return redirect("/dashboard")

@app.route('/messages/send_message',methods=["POST"])
def send_message():
    if not message.Message.validate_message(request.form):
      return redirect('/')
    data = {
      "user_from_id":session["user_id"],
      "user_to_id":request.form["user_to_id"],
      "text":request.form["text"]
    }
    message.Message.save(data)
    flash("Message sent","success")
    return redirect("/dashboard")


@app.route('/error_attempt')
def error_attempt():
    if session["num_attempt"] > 1:
      session.clear()
      return redirect("/")
    return render_template("/error.html")

