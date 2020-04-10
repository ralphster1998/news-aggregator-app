import React, { Component } from 'react'
import jwt_decode from 'jwt-decode'

class Profile extends Component {
    constructor() {
        super()
        this.state = {
            username: '',
            urls:[]
        }
    }

    componentDidMount () {
        const token = localStorage.usertoken
        const decoded = jwt_decode(token)
        console.log("Check: " + decoded.identity.urls)
        this.setState({
            username: decoded.identity.username,
            urls: decoded.identity.urls
        })
    }

    render () {
        const URLS = this.state.urls;
        const listURLs = URLS.map((url) =>
        <ul>{url}</ul>
        );
        return (
            <div className="container">
                <div className="jumbotron mt-5">
                    <div className="col-sm-8 mx-auto">
                        <h1 className="text-center">PROFILE</h1>
                    </div>
                    <table className="table col-md-6 mx-auto">
                        <tbody>
                            <tr>
                                <td>Username</td>
                                <ul>{this.state.username}</ul>
                            </tr>
                            <tr>
                                <td>URLs</td>
                                {listURLs}
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
}

export default Profile