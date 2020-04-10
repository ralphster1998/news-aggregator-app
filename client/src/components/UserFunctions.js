import axios from 'axios'

// newUser comes from the form
// payload method is inside the post; accepts the payload
export const register = newUser => {
    return axios
        .post("api/register", {
            username: newUser.username,
            password: newUser.password,
            urls: newUser.urls
        })
        .then(response => {
            console.log("Registered")
        })
}

// accepts an object
export const login = user => {
    return axios
        .post("api/login", {
            username: user.username,
            password: user.password
        })
        .then(response => {
            localStorage.setItem('usertoken', response.data.token)
            return response.data.token
        })
        .catch(err => {
            console.log(err)
        })
}