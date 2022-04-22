console.log("follows.js")

const nonFollowedDIV = document.querySelector('.unfollowed-list')
const followedDIV = document.querySelector('.followed-list')

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
        console.log("Success", data);
        // 200 OK
        if (data.usersGet) {
            console.log("All good.")

            // create not followed user in HTML 
            data.usersNotFollowed.forEach(userNotFollowed => {
                let userHTML = createHTMLForNonFollowing(userNotFollowed.userId, userNotFollowed.userFirstName, userNotFollowed.userLastName, userNotFollowed.userEmail, userNotFollowed.tweetAmount || "0")
                nonFollowedDIV.insertAdjacentHTML("afterbegin", userHTML)
            })

            // create followed users in HTML
            data.usersFollowed.forEach(userFollowed => {
                let userHTML = createHTMLForFollowing(userFollowed.userId, userFollowed.userFirstName, userFollowed.userLastName, userFollowed.userEmail)
                followedDIV.insertAdjacentHTML("afterbegin", userHTML)
            })
        }
    })
    .catch((error) => {
        console.error(error)
    })
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// Other Methods
function createHTMLForFollowing(id, name, surname, email) {
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
            </div>
        </div>
    `
}

function createHTMLForNonFollowing(id, name, surname, email, tweetsCount) {
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
                
                <p class="user-tweet-count">${tweetsCount} tweets</p>
            </div>
        </div>
    `
}