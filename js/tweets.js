// Global variables
let DELETE_TWEET_ID = String;
let UPDATE_TWEET_ID = String;
let LIKE_TWEET_ID = String;
let UNLIKE_TWEET_ID = String;
let likeTweetButtons = NodeList; 
let unlikeTweetButtons = NodeList;
let deleteTweetButtons = NodeList;
let ownedTweets = NodeList;

// Buttons
const submitCreateTweet = document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-bottom-section-button-create-tweet');
const submitUpdateTweet = document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-bottom-section-button-update-tweet');
const openTweetForm = document.querySelector('.home-page-column-1-tweet-button');
const noDeleteButton = document.querySelector('.home-page-column-2-pop-up-delete-tweet-buttons-no');
const yesDeleteButton = document.querySelector('.home-page-column-2-pop-up-delete-tweet-buttons-yes');

// Div
const tweetsDIV = document.querySelector('.home-page-column-2-tweets');

/////////////////////////////////////////////////
// Methods
function getTweetByUserID(id) {
    apiGetTweetByUserID(id);
};

function createTweet() {
    // Create form data
    let formData = new FormData();

    // Collect inputs and form FormData
    formData.append('user-id', USER_ID);
    formData.append('title' , document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-title-input').value);
    formData.append('description', document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-description-input').value);
    if (document.querySelector('#create-tweet-upload-image').files[0])
        formData.append('image', document.querySelector('#create-tweet-upload-image').files[0])

    // fetch
    apiPostTweet(formData, USER_ID);
}

function updateTweet() {
    submitUpdateTweet.disabled = true;
    submitUpdateTweet.innerText = 'Updating';
    // Create form data
    let formData = new FormData();

    // Collect inputs and form FormData
    formData.append('user-id', USER_ID);
    formData.append('title' , document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-title-input').value);
    formData.append('description', document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-description-input').value);
    if (document.querySelector('#create-tweet-upload-image').files[0])
        formData.append('image', document.querySelector('#create-tweet-upload-image').files[0])

    // fetch
    apiPatchTweetByTweetID(UPDATE_TWEET_ID, formData); 
}       

function closeCreateTweetPopupAndHomeOverlay() {
    closeHomeOverlay();
    closeTweetFormPopup();
};

function closeDeleteTweetPopupAndHomeOverlay() {
    closeHomeOverlay();
    closeTweetDeletePopup();
};
/////////////////////////////////////////////////
// Async Methods
async function apiGetTweetByUserID(id) {
    fetch('/api/tweets/user/' + id, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {

        // OK 200
        if (data.tweetsFound) {
            let tweets = data.tweets;
            tweets.forEach(tweet => {
                let tweetHTML = createHTMLForTweet(tweet.tweetImageUrl !== "", tweet.userId === id, tweet.tweetId, tweet.userFirstName, tweet.userLastName, tweet.userUsername, tweet.tweetUpdatedAt || tweet.tweetCreatedAt, tweet.tweetTitle, tweet.tweetDescription, tweet.tweetImageUrl, tweet.liked, tweet.likes);
                tweetsDIV.insertAdjacentHTML('afterbegin', tweetHTML);
            });
            // After creating tweets in DOM attach event listener to their delete buttons
            deleteTweetButtons = document.querySelectorAll('#tweet-right-top-options');
            attachDeleteEventListeners(deleteTweetButtons);

            // After creatint tweets in DOM attach event listener to tweet for update
            ownedTweets = document.querySelectorAll(".own");
            attachUpdateEventListeners(ownedTweets);

            // After creating tweets in DOM attach event listener to tweet for update
            likeTweetButtons = document.querySelectorAll('#like-button');
            attachLikeEventListeners(likeTweetButtons);
        };
    })
    .catch((error) => {
        console.log("Error", error);
    });
};

async function getTweetByTweetID() {
    // fetch
    fetch(`/api/tweets/user/${USER_ID}/tweet/${UPDATE_TWEET_ID}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);

        // 200 OK
        if (data.tweetFound) {
            // Put values of the found data to form
            document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-title-input').value = data.tweet.tweetTitle;
            document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-description-input').value = data.tweet.tweetDescription;
            // Hide Update button
            submitCreateTweet.classList.add('hidden');
            // Open tweet form
            openTweetFormPopup();
        }
    })
    .catch((error) => {
        console.log("Error", error);
    });
}

async function apiPostTweet(form, id) {
    // fetch
    fetch('/api/tweets', {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);

        // 200 OK
        if (data.tweetAdded) {
            // Build tweet 
            let tweetHTML = createHTMLForTweet(data.tweet.tweetImageUrl !== "", data.tweet.userId === id, data.tweet.tweetId, data.user.userFirstName, data.user.userLastName, data.user.userUsername, data.tweet.tweetUpdatedAt || data.tweet.tweetCreatedAt, data.tweet.tweetTitle, data.tweet.tweetDescription, data.tweet.tweetImageUrl);
            tweetsDIV.insertAdjacentHTML("afterbegin", tweetHTML);

            // After creating tweet in DOM attach event listener to his  delete buttons
            deleteTweetButtons = document.querySelectorAll('#tweet-right-top-options');
            attachDeleteEventListeners(deleteTweetButtons);

            // After creating tweets in DOM attach event listener to tweet for update
            ownedTweets = document.querySelectorAll(".own");
            attachUpdateEventListeners(ownedTweets);

            // After creating tweets in DOM attach event listener to tweet for update
            likeTweetButtons = document.querySelectorAll('#like-button');
            attachLikeEventListeners(likeTweetButtons);

            // Clear inputs
            document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-title-input').value = "";
            document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-description-input').value = "";
            document.querySelector('#create-tweet-upload-image').value = null;
            document.querySelector('#create-tweet-upload-image').files[0] = null;

            submitCreateTweet.classList.remove('hidden');
            submitUpdateTweet.classList.remove('hidden');
            closeCreateTweetPopupAndHomeOverlay();
        }
        
        // Reset button
        submitCreateTweet.disabled = false;
        submitCreateTweet.innerText = "Tweet";
    })
    .catch((error) => {
        console.log("Error", error);
    });
}

async function apiDeleteTweetByTweetID(id) {
    // fetch
    console.log(USER_ID, id);
    fetch(`api/tweets/user/${USER_ID}/tweet/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);

        // 200 OK
        if (data.tweetDeleted) {
            console.log("Deleted tweet", data.tweetDeleted);

            // Remove deleted tweet in DOM
            let deletedTweet = document.getElementById(data.tweetId);
            deletedTweet.remove();
        }

        yesDeleteButton.disabled = false;
        yesDeleteButton.innerText = 'Yes';
        // Close delete tweet pop-up
        closeDeleteTweetPopupAndHomeOverlay();
    })
    .catch((error) => {
        console.log("Error", error);
    });
}

async function apiPatchTweetByTweetID(id, form) {
    // fetch
    fetch('/api/tweets/' + id, {
        method: 'PATCH',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);
        // OK 200
        if (data.tweetUpdated) {
            // Change tweet in DOM
            let target = document.getElementById(data.tweet.tweetId);
            target.remove();

            let updatedTweetHTML = createHTMLForTweet(data.tweet.tweetImageUrl !== "", data.tweet.userId === USER_ID, data.tweet.tweetId, data.user.userFirstName, data.user.userLastName, data.user.userUsername, data.tweet.tweetUpdatedAt || data.tweet.tweetCreatedAt, data.tweet.tweetTitle, data.tweet.tweetDescription, data.tweet.tweetImageUrl);
            tweetsDIV.insertAdjacentHTML("afterbegin", updatedTweetHTML);

            // After creating tweet in DOM attach event listener to his  delete buttons
            deleteTweetButtons = document.querySelectorAll('#tweet-right-top-options');
            attachDeleteEventListeners(deleteTweetButtons);

            // After creatint tweets in DOM attach event listener to tweet for update
            ownedTweets = document.querySelectorAll(".own");
            attachUpdateEventListeners(ownedTweets);

            // After creating tweets in DOM attach event listener to tweet for update
            likeTweetButtons = document.querySelectorAll('#like-button');
            attachLikeEventListeners(likeTweetButtons);

            // Close 
            closeCreateTweetPopupAndHomeOverlay();
            // Reset values
            document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-title-input').value = "";
            document.querySelector('.home-page-column-2-pop-up-tweet-form-content-right-description-input').value = "";
            document.querySelector('#create-tweet-upload-image').value = null;
            document.querySelector('#create-tweet-upload-image').files[0] = null;
        }
            // Unhide buttons 
            submitUpdateTweet.disabled = false;
            submitUpdateTweet.innerText = 'Update';
            submitCreateTweet.classList.remove('hidden');
        submitUpdateTweet.classList.remove('hidden');
    })
    .catch((error) => {
        console.log("Error", error);
    });
} 

async function apiLike(userId, tweetId, button) {
    // create form data
    let formData = new FormData();
    formData.append('user_id', userId);
    formData.append('tweet_id', tweetId);
    
    // fetch
    fetch('/api/likes', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);
        
        // 200 OK
        if (data.liked) {
            // increment like count in DOM
            let likeString = "  0";
            if (!button.innerText === "")
                likeString = button.innerText;
            let likeCount = parseInt(likeString);
            likeCount += 1;
    
            // change button in html
            // insert unlike button
            let unlikeButton = createHTMLForUnlikeButton(likeCount);
            button.insertAdjacentHTML("beforebegin", unlikeButton);
            // delete like button
            button.remove();
    
            // add event listeners to unlike buttons
            unlikeTweetButtons = document.querySelectorAll('#unlike-button');
            attachUnlikeEventListeners(unlikeTweetButtons);
        }
    })
    .catch((error) => {
        console.log(error);
    });
};

async function apiUnlike(userId, tweetId, button) {
    // fetch
    fetch(`/api/likes/user/${userId}/tweet/${tweetId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);

        // 200 OK
        if (data.likeDeleted) {
            // decrement like count in DOM
            let likeString = button.innerText;
            let likeCount = parseInt(likeString);
            likeCount -= 1;

            // change button in html
            // insert like button
            let likeButton = createHTMLForLikeButton(likeCount);
            button.insertAdjacentHTML("beforebegin", likeButton);
            // remove unlike button
            button.remove();

            // add event listeners to like buttons
            unlikeTweetButtons = document.querySelectorAll('#unlike-button');
            attachUnlikeEventListeners(unlikeTweetButtons);
        }
    })
    .catch((error) => {
        console.log("Error", error);
    });

};
/////////////////////////////////////////////////
// Event listeners
openTweetForm.addEventListener('click', () => {
    submitUpdateTweet.classList.add('hidden');
    goToTweetForm();
});

submitCreateTweet.addEventListener('click', () => {
    submitCreateTweet.disabled = true;
    submitCreateTweet.innerText = "Tweeting";
    createTweet();
});

noDeleteButton.addEventListener('click', () => {
    closeDeleteTweetPopupAndHomeOverlay();
});

yesDeleteButton.addEventListener('click', () => {
    yesDeleteButton.disabled =  true;
    yesDeleteButton.innerText = 'Deleting...';
    apiDeleteTweetByTweetID(DELETE_TWEET_ID);
});

submitUpdateTweet.addEventListener('click', () => {
    updateTweet();
});

/////////////////////////////////////////////////
// For-each event listeners
function attachDeleteEventListeners(nodeList) {
    nodeList.forEach(deleteButton => {
        deleteButton.addEventListener('click', () => {
            DELETE_TWEET_ID = deleteButton.parentElement.parentElement.parentElement.id;
            // Open home overlay
            openHomeOverlay();

            // Open menu
            openTweetDeletePopup();
        });
    });
};

function attachUpdateEventListeners(nodeList) {
    nodeList.forEach(updateButton => {
        updateButton.addEventListener('click', () => {
            UPDATE_TWEET_ID =  updateButton.parentElement.parentElement.id;
            // Open Home overlay
            openHomeOverlay();
            
            // Get tweet values by id
            getTweetByTweetID();
        });
    });
}

function attachLikeEventListeners(nodeList) {
    nodeList.forEach(likeButton => {
        likeButton.addEventListener('click', () => {
            LIKE_TWEET_ID = likeButton.parentElement.parentElement.parentElement.id;
            
            // disable like button
            likeButton.disabled = true;

            // call api method
            apiLike(USER_ID, LIKE_TWEET_ID, likeButton);
        })
    });
};

function attachUnlikeEventListeners(nodeList) {
    nodeList.forEach(unlikeButton => {
        unlikeButton.addEventListener('click', () => {
            UNLIKE_TWEET_ID = unlikeButton.parentElement.parentElement.parentElement.id;
            console.log(UNLIKE_TWEET_ID);

            // disable unlike button
            unlikeButton.disabled = true;

            // call api method
            apiUnlike(USER_ID, UNLIKE_TWEET_ID, unlikeButton);
        });
    });
};

tweetCreateExitButton.addEventListener('click', () => {
    closeCreateTweetPopupAndHomeOverlay();
});

/////////////////////////////////////////////////
// Other methods
function createHTMLForLikeButton (likeCount) {
    return `<i id="like-button" class="fa fa-heart-o">  ${likeCount}</i>`;
};

function createHTMLForUnlikeButton(likeCount) {
    return `<i id="unlike-button" class="fa fa-heart">  ${likeCount}</i>`;
};

function createHTMLForTweet(booleanImage, booleanButton, id, name, surname, username, date, title, description, imageUrl, liked, likes) {
    let HTMLForLikeButton =  `<i id="like-button" class="fa fa-heart">  ${likes}</i>`
    if (likes == undefined) {
        likes = "";
        HTMLForLikeButton = `<i id="like-button" class="fa fa-heart-o">  ${likes}</i>`;
    } 
    
    if (booleanImage === false && booleanButton === false) {
        return ` 
        <div id="${id}" class="tweet">
                <div class="tweet-left">
                    <img class="tweet-user-icon" src="/illustrations/user.png" alt="User photo">
                </div>
                <div class="tweet-right">
                    <div class="tweet-right-top">
                        <p class="tweet-right-top-name">${name} ${surname}</p>
                        <p class="tweet-right-top-username">${username}<p>
                        <p>·</p>
                        <p class="tweet-right-top-date">${date}</p>
                    </div>
                    <div class="tweet-right-content">
                        <p class="tweet-right-content-title">${title}</p>
                        <p class="tweet-right-content-description">${description}</p>
                    </div>
                    <div class="tweet-right-bottom">
                        ${HTMLForLikeButton}
                    </div>
                </div>
            </div>
        </div>
        `;
    } if (booleanImage === true && booleanButton === false) {
        return ` 
        <div id="${id}" class="tweet">
                <div class="tweet-left">
                    <img class="tweet-user-icon" src="/illustrations/user.png" alt="User photo">
                </div>
                <div class="tweet-right">
                    <div class="tweet-right-top">
                        <p class="tweet-right-top-name">${name} ${surname}</p>
                        <p class="tweet-right-top-username">${username}<p>
                        <p>·</p>
                        <p class="tweet-right-top-date">${date}</p>
                    </div>
                    <div class="tweet-right-content">
                        <p class="tweet-right-content-title">${title}</p>
                        <p class="tweet-right-content-description">${description}</p>
                    </div>
                    <div class="tweet-right-image-div">
                        <img class="tweet-image" src="/images/${imageUrl}" alt="Image">
                    </div>
                    <div class="tweet-right-bottom">
                        ${HTMLForLikeButton}
                    </div>
                </div>
            </div>
        </div>
        `;
    } if (booleanImage === false && booleanButton === true) {
        return `
        <div id="${id}" class="tweet">
                <div class="tweet-left">
                    <img class="tweet-user-icon" src="/illustrations/user.png" alt="User photo">
                </div>
                <div class="tweet-right">
                    <div class="tweet-right-top">
                        <p class="tweet-right-top-name">${name} ${surname}</p>
                        <p class="tweet-right-top-username">${username}<p>
                        <p>·</p>
                        <p class="tweet-right-top-date">${date}</p>
                        <i id="tweet-right-top-options" class="fa fa-ellipsis-h"></i>
                    </div>
                    <div class="tweet-right-content own">
                        <p class="tweet-right-content-title">${title}</p>
                        <p class="tweet-right-content-description">${description}</p>
                    </div>
                    <div class="tweet-right-bottom">
                        ${HTMLForLikeButton}
                    </div>
                </div>
            </div>
        </div>
        `;
    } else 
        return `
        <div id="${id}" class="tweet">
                <div class="tweet-left">
                    <img class="tweet-user-icon" src="/illustrations/user.png" alt="User photo">
                </div>
                <div class="tweet-right">
                    <div class="tweet-right-top">
                        <p class="tweet-right-top-name">${name} ${surname}</p>
                        <p class="tweet-right-top-username">${username}<p>
                        <p>·</p>
                        <p class="tweet-right-top-date">${date}</p>
                        <i id="tweet-right-top-options" class="fa fa-ellipsis-h"></i>
                    </div>
                    <div class="tweet-right-content own">
                        <p class="tweet-right-content-title">${title}</p>
                        <p class="tweet-right-content-description">${description}</p>
                        <img class="tweet-image" src="/images/${imageUrl}" alt="Image">
                    </div>
                    <div class="tweet-right-bottom">
                        ${HTMLForLikeButton}
                    </div>
                </div>
            </div>
        </div>
        `;
}