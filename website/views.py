from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Post, User, Comment, Like

views=Blueprint('views', __name__)

@views.route("/")
@views.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    # posts=Post.query.all()
    posts=Post.query.order_by(Post.date_created.desc()).all()    
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method=='POST':
        text= request.form.get('text')       

        if not text:
            flash("Posts can't be empty.", category="error")
        else: 
            #Create a Post object and initialize it
            post=Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post has been published!", category="success")

            # for post in current_user.posts:
            #     print(post.text)
            #     print(post.user.username)        
            #     print()
                
            return redirect(url_for('views.home'))

    return render_template("create-post.html", user=current_user)


#dynamic route
# value is fetched from <...> and can be passed to function for appropriate action.
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post=Post.query.filter_by(id=id).first()

    #verify post exists -> then whether the user has privilege to delete it -> then finally delete
    if not post:
        flash("Post doesn't exist.", category='error')            
    elif (current_user.id!=post.author):
        flash("you do not have permission to delete this post", category='error')    
    else:
        db.session.delete(post)
        db.session.commit()
        flash("post has been deleted", category='error')

    return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def user_posts(username):
    user_exists=User.query.filter_by(username=username).first()

    if not user_exists:
        flash("User doesn't exist", category='error')
        return redirect(url_for('views.home'))
    
    #list of all posts by user <user_exists>
    #posts=Post.query.filter_by(author=user_exists.id).all()     
    posts=user_exists.posts
    return render_template("posts.html", posts=posts, user=current_user, username=username)


@views.route("/create-comment/<post_id>", methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    post=Post.query.filter_by(id=post_id).first()

    if not post:
        flash("Post doesn't exist", category='error')        
    else:
        text=request.form.get("text")
        if not text:
            flash("Comment can't be empty", category='error')                        
        else:    
            comment=Comment(text=text, author=current_user.id, post_id=post_id)

            db.session.add(comment)        
            db.session.commit()                  
            flash(f"Comment sent to {post.user.username}")    
    
    #return redirect(request.referrer or url_for('views.home'))
    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment_exists=Comment.query.filter_by(id=comment_id).first()      

    if not comment_exists:
        flash("comment doesn't exist", category='error')
    elif comment_exists.user.id!=current_user.id:
        flash("You do not have permission to delete this comment", category='error')
    else:
        db.session.delete(comment_exists)
        db.session.commit()
        flash("comment deleted", category='success')        
    return redirect(url_for('views.home'))




# methods=['GET']
#@views.route("/like-post/<post_id>")
'''
@login_required
def like_post(post_id):
    post_exists=Post.query.filter_by(id=post_id)    
    # you should use db.session.delete(like_exists.first()) instead of db.session.delete(like_exists) 
    # This ensures that you're deleting the actual like object, not the query object.
    like_exists=Like.query.filter_by(post_id=post_id, author=current_user.id).first()

    if not post_exists:
        flash("post doesnt't exist", category='error')    
    elif like_exists:        
        db.session.delete(like_exists)
        db.session.commit()
        flash(f"{current_user.username} unliked the post", category='success')
    else:
        like=Like(post_id=post_id, author=current_user.id)    
        db.session.add(like)        
        db.session.commit()
        flash(f"{current_user.username} liked the post", category='success')
    
    return redirect(url_for('views.home'))

'''


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like_post(post_id):    
    post_exists=Post.query.filter_by(id=post_id).first()
    # you should use db.session.delete(like_exists.first()) instead of db.session.delete(like_exists) 
    # This ensures that you're deleting the actual like object, not the query object.
    like_exists=Like.query.filter_by(post_id=post_id, author=current_user.id).first()

    if not post_exists:
        # flash("post doesnt't exist", category='error')    
        return jsonify({"error": "Post doesn't exist"}, 400)    #error code
    elif like_exists:        
        db.session.delete(like_exists)
        db.session.commit()
        # flash(f"{current_user.username} unliked the post", category='success')
    else:
        like=Like(post_id=post_id, author=current_user.id)    
        db.session.add(like)        
        db.session.commit()
        # flash(f"{current_user.username} liked the post", category='success')

    return jsonify({"likes": len(post_exists.likes),"liked": bool( not like_exists)})
    # return jsonify({"likes": len(post_exists.likes),"liked": current_user.id in map(lambda x: x.author, post_exists.likes)})        

