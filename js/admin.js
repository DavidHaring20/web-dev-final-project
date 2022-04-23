
// Global variables
let DELETE_ADMIN_TWEET_STRING = String
let DELETE_ADMIN_TWEET_ID = String
let ADMIN_TWEETS = NodeList

// Overlay
const adminTweetsOverlay = document.querySelector('.admin-overlay')

// Pop-up Window
const deleteAdminTweetPopup = document.querySelector('.admin-page-pop-up-delete-tweet')

// HTML Element - DIV
const allTweetsAdminDIV = document.querySelector('.admin-page-tweets-div')

// HTML Elements - BUTTONS
const yesDeleteAdminTweetBUTTON = document.querySelector('.admin-page-pop-up-delete-tweet-buttons-yes')
const noDeleteAdminTweetBUTTON = document.querySelector('.admin-page-pop-up-delete-tweet-buttons-no')

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// API Methods
async function apiGetAllTweets() {
    // Fetch
    fetch('/api/tweets/admin/' + USER_ID, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // 200 OK
        if (data.tweetsFound) {
            data.tweets.forEach(tweet => {
                let tweetHTML = createHTMLForAdminTweet(tweet.tweetId, tweet.tweetTitle, tweet.tweetDescription, tweet.tweetImageUrl)
                allTweetsAdminDIV.insertAdjacentHTML("afterbegin", tweetHTML)
            })

            // Attach Event Listeners to Tweets
            ADMIN_TWEETS = document.querySelectorAll('.admin-tweet')
            attachEventListeners(ADMIN_TWEETS)
        }
    })
    .catch((error) => {
        console.error("Error", error)
    })
}

async function apiDeleteTweetAdmin() {
    // Fetch
    fetch(`/api/tweets/admin/${USER_ID}/tweet/${DELETE_ADMIN_TWEET_ID}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data)

        // 200 OK
        if (data.tweetDeleted) {
            // Remove Deleted tweet from DOM
            document.getElementById(DELETE_ADMIN_TWEET_STRING).remove()
        }

        // Close pop-up window
        deleteAdminTweetPopup.classList.add('hidden')
        
        // Close Admin overlay
        adminTweetsOverlay.classList.add('hidden')

        // Revert button
        yesDeleteAdminTweetBUTTON.innerText = 'Yes'
        yesDeleteAdminTweetBUTTON.style.backgroundColor = '#1DA1F2'
        yesDeleteAdminTweetBUTTON.disabled = false
    })
    .catch((error) => {
        console.error("Error", error)
    })
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Attach Event Listers Methods

function attachEventListeners(nodeList) {
    nodeList.forEach(node => {
        node.addEventListener('click', () => {
            window.scroll(0 ,0)
            DELETE_ADMIN_TWEET_STRING = node.id           
            // ID of Tweet is admin-tweet-${id}
            // Remove "admin-tweet-" from id 
            DELETE_ADMIN_TWEET_ID = DELETE_ADMIN_TWEET_STRING.replace('admin-tweet-', "") 

            // Open Admin overlay
            adminTweetsOverlay.classList.remove('hidden')

            // Open pop-up window
            deleteAdminTweetPopup.classList.remove('hidden')
        })
    })
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Event Listers 

adminTweetsOverlay.addEventListener('click', () => {
    // Close pop-up window
    deleteAdminTweetPopup.classList.add('hidden')
    
    // Close Admin overlay
    adminTweetsOverlay.classList.add('hidden')
})

yesDeleteAdminTweetBUTTON.addEventListener('click', () => {
    // Disable button
    yesDeleteAdminTweetBUTTON.innerText = 'Deleting...'
    yesDeleteAdminTweetBUTTON.style.backgroundColor = '#AAB8C2'
    yesDeleteAdminTweetBUTTON.disabled = true

    // Call Api method
    apiDeleteTweetAdmin()
}) 

noDeleteAdminTweetBUTTON.addEventListener('click', () => {
    // Close pop-up window
    deleteAdminTweetPopup.classList.add('hidden')
    
    // Close Admin overlay
    adminTweetsOverlay.classList.add('hidden')
})

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Other Methods

function createHTMLForAdminTweet(id, title, description, imageUrl) {
    return `
    <div class="admin-tweet" id="admin-tweet-${id}">
        <div class="admin-tweet-content">
            <h4 class="admin-tweet-title">${title}</h4>
            <p class="admin-tweet-description">${description}</p>

            <img class="admin-tweet-image" src="/images/${imageUrl}" alt="Image">
        </div>
    </div>
    `
}