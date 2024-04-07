// Javascript --> camelcase
// console.log(post_id)    --> to print something on inspect.console

function likePost(postId){    
    const likesCount=document.getElementById(`likes-count-${postId}`)
    const likeButton=document.getElementById(`like-button-${postId}`)
    
    fetch(`/like-post/${postId}`, {method: `POST`})
        .then((res) => res.json())
        .then((data) =>{            
            console.log(data)
            likesCount.innerHTML=data[`likes`]
            if(data[`liked`]==true){
                likeButton.className= `fa-solid fa-thumbs-up fa-xl`
            }            
            else{
                likeButton.className= `fa-regular fa-thumbs-up fa-xl`
            }
        
    })
    // console.log(likesCount.value)
    .catch((e) => alert(`Failure: post couldn't be liked.`))
}

function createComment(postId){
    
    // .catch((e) => alert(`Failure: Comment couldn't be created`));
}