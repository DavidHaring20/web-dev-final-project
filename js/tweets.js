console.log('tweets.js');

// Buttons
const openTweetForm = document.querySelector('.home-page-column-1-tweet-button');
const tweetsDIV = document.querySelector('.home-page-column-2-tweets');
getTweetByUserID();
/////////////////////////////////////////////////
// Methods
function getTweetByUserID() {
    apiGetTweetByUserID();
};
/////////////////////////////////////////////////
// Async Methods
async function apiGetTweetByUserID(id='6facbefe-5493-4011-b58e-04aa69515bba') {
    fetch('/api/tweets/user/' + id, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);

        // OK 200
        if (data.tweetsFound) {
            let tweets = data.tweets;
            tweets.forEach(tweet => {
                let tweetHTML = createHTMLForTweet(tweet.tweetImageUrl !== "", tweet.userId === '6facbefe-5493-4011-b58e-04aa69515bba', tweet.userId, tweet.userFirstName, tweet.userLastName, tweet.userUsername, tweet.tweetUpdatedAt || tweet.tweetCreatedAt, tweet.tweetTitle, tweet.tweetDescription, tweet.tweetImageUrl);
                console.log(tweet.tweetTitle, tweet.userId === '6facbefe-5493-4011-b58e-04aa69515bba')
                tweetsDIV.insertAdjacentHTML('afterbegin', tweetHTML);
            });
        };
    })
    .catch((error) => {
        console.log("Error", error);
    });
};
/////////////////////////////////////////////////
// Event listeners
openTweetForm.addEventListener('click', () => {
    goToTweetForm();
});

/////////////////////////////////////////////////
// Other methods
function createHTMLForTweet(booleanImage, booleanButton, id, name, surname, username, date, title, description, imageUrl) {
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
                        <i class="fa fa-heart-o"></i>
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
                        <i class="fa fa-heart-o"></i>
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
                    <div class="tweet-right-content">
                        <p class="tweet-right-content-title">${title}</p>
                        <p class="tweet-right-content-description">${description}</p>
                    </div>
                    <div class="tweet-right-bottom">
                        <i class="fa fa-heart-o"></i>
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
                    <div class="tweet-right-content">
                        <p class="tweet-right-content-title">${title}</p>
                        <p class="tweet-right-content-description">${description}</p>
                    </div>
                    <div class="tweet-right-image-div">
                        <img class="tweet-image" src="/images/${imageUrl}" alt="Image">
                    </div>
                    <div class="tweet-right-bottom">
                        <i class="fa fa-heart-o"></i>
                    </div>
                </div>
            </div>
        </div>
        `;
}