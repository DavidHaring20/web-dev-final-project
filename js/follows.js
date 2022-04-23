// Global Variables
let FOLLOW_ID = String;
let UNFOLLOW_ID = String;
let FOLLOWED_USERS = NodeList;
let NON_FOLLOWED_USERS = NodeList;

// HTML Elements - DIV
const nonFollowedDIV = document.querySelector('.unfollowed-list')
const followedDIV = document.querySelector('.followed-list')

// HTML Elements - BUTTON
const yesFollowBUTTON = document.querySelector('.home-page-column-3-follow-unfollow-buttons-yes-start-follow')
const yesUnfollowBUTTON = document.querySelector('.home-page-column-3-follow-unfollow-buttons-yes-end-follow')
const noBUTTON = document.querySelector('.home-page-column-3-follow-unfollow-buttons-no')

// HTML Elements - P
const followP = document.querySelector('.home-page-column-3-follow-unfollow-content-p-start-follow')
const unfollowP = document.querySelector('.home-page-column-3-follow-unfollow-content-p-end-follow')

apiGetUsers()

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// API Methods
async function apiGetUsers() {
    // Fetch
    fetch('/api/users/' + USER_ID, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // 200 OK
        if (data.usersGet) {
            // Create non-followed users in HTML 
            data.usersNotFollowed.forEach(userNotFollowed => {
                let userHTML = createHTMLForNonFollowing(userNotFollowed.userId, userNotFollowed.userFirstName, userNotFollowed.userLastName, userNotFollowed.userEmail, userNotFollowed.userUsername,userNotFollowed.tweetAmount || "0")
                nonFollowedDIV.insertAdjacentHTML("afterbegin", userHTML)
            })

            // Attach Event Listener to Non-followed users
            NON_FOLLOWED_USERS = document.querySelectorAll('.not-following')
            attachEventListenerNonFollowed(NON_FOLLOWED_USERS)

            // Create followed users in HTML
            data.usersFollowed.forEach(userFollowed => {
                let userHTML = createHTMLForFollowing(userFollowed.userId, userFollowed.userFirstName, userFollowed.userLastName, userFollowed.userEmail, userFollowed.userUsername)
                followedDIV.insertAdjacentHTML("afterbegin", userHTML)
            })

            // Attach Event Listener to Followed users
            FOLLOWED_USERS = document.querySelectorAll('.following')
            attachEventListenerFollowed(FOLLOWED_USERS)
        }
    })
    .catch((error) => {
        console.error(error)
    })
}

async function apiPostFollow(followerID, followedID) {
    // Create form 
    let form = new FormData()
    form.append("follower_user_id", followerID)
    form.append("followed_user_id", followedID)
    // Fetch
    fetch('/api/follows', {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data)
        // Hide Follow/Unfollow pop-up and Home overlay
        closeFollowUnfollow()
        closeHomeOverlay()

        // Remove hide from Button and Paragraph which are used in unfollowing pop-up
        yesUnfollowBUTTON.classList.remove('hidden')
        unfollowP.classList.remove('hidden')

    })
    .catch((error) => {
        console.error("Error", error)
    })
}

async function apiDeleteFollow(followerID, followedID) {
    // Fetch
    fetch(`/api/follows/follower_user_id/${followerID}/followed_user_id/${followedID}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data)
        // Hide Follow/Unfollow pop-up and Home overlay
        closeFollowUnfollow()
        closeHomeOverlay()

        // Remove hide from Button and Paragraph which are used in following pop-up
        yesFollowBUTTON.classList.remove('hidden')
        unfollowP.classList.remove('hidden')
    })
    .catch((error) => {
        console.error("Error", error)
    })
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Attach Event listeners

function attachEventListenerFollowed(nodeList) {
    nodeList.forEach(node => {
        node.addEventListener('click', () => {
            UNFOLLOW_ID = node.id;

            // Hide Button and Paragraph which are used in following pop-up
            yesFollowBUTTON.classList.add('hidden')
            followP.classList.add('hidden')

            // Open Home OVerlay
            openHomeOverlay()

            // Open pop-up window
            openFollowUnfollowPopup()
        })
    })
}

function attachEventListenerNonFollowed(nodeList) {
    nodeList.forEach(node => {
        node.addEventListener('click', () => {
            FOLLOW_ID = node.id;

            // Hide Button and Paragraph which are used in unfollowing pop-up
            yesUnfollowBUTTON.classList.add('hidden')
            unfollowP.classList.add('hidden')

            // Open Home Overlay
            openHomeOverlay()

            // Open pop-up window
            openFollowUnfollowPopup()
        })
    })
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Event listeners

homeOverlay.addEventListener('click', () => {
    closeFollowUnfollow()
    // Remove hide from Button and Paragraph which are used in unfollowing pop-up
    yesUnfollowBUTTON.classList.remove('hidden')
    yesFollowBUTTON.classList.remove('hidden')
    unfollowP.classList.remove('hidden')
    followP.classList.remove('hidden')
})

yesUnfollowBUTTON.addEventListener('click', () => {
    apiDeleteFollow(USER_ID, UNFOLLOW_ID)
}) 

yesFollowBUTTON.addEventListener('click', () => {
    apiPostFollow(USER_ID, FOLLOW_ID)
})

noBUTTON.addEventListener('click', () => {
    closeFollowUnfollow()
    closeHomeOverlay()
    // Remove hide from Button and Paragraph which are used in unfollowing pop-up
    yesUnfollowBUTTON.classList.remove('hidden')
    yesFollowBUTTON.classList.remove('hidden')
    unfollowP.classList.remove('hidden')
    followP.classList.remove('hidden')
})

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Other Methods
function createHTMLForFollowing(id, name, surname, email, username) {
    return `
        <div id="${id}" class="user following">
            <div class="user-top-section">
                <div class="user-top-section-content">
                    <p class="user-top-section-name">${name}</p>
                    <p class="user-top-section-surname">${surname}</p>
                    <p class="user-top-section-dot">·</p>
                    <p class="user-top-section-dot-status">Trending</p>
                    
                    <div class="user-top-section-more">
                        <i class="fa fa-ellipsis-h"></i>
                    </div>
                </div>
            </div>

            <div class="user-content">
                <h4 class="user-content-email">${email}</h4>

                <p class="user-content-username">@${username}</p>
            </div>
        </div>
    `
}

function createHTMLForNonFollowing(id, name, surname, email, username,tweetsCount) {
    return `
        <div id="${id}" class="user not-following">
            <div class="user-top-section">
                <div class="user-top-section-content">
                    <p class="user-top-section-name">${name}</p>
                    <p class="user-top-section-surname">${surname}</p>
                    <p class="user-top-section-dot">·</p>
                    <p class="user-top-section-dot-status">Trending</p>
                    
                    <div class="user-top-section-more">
                        <i class="fa fa-ellipsis-h"></i>
                    </div>
                </div>
            </div>

            <div class="user-content">
                <h4 class="user-content-email">${email}</h4>

                <p class="user-content-username">@${username}</p>
                
                <p class="user-tweet-count">${tweetsCount} tweets</p>
            </div>
        </div>
    `
}