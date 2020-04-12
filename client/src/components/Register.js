import React, { Component } from 'react'
import { register } from './UserFunctions'
import { Dropdown } from 'semantic-ui-react'

const data = [
    { key: 'tech_radar', text: 'Tech Radar', value: 'Tech Radar' },
    { key: 'medical', text: 'Medical News Today', value: 'Medical News Today' },
    { key: 'buzzfeed', text: 'Buzz Feed News', value: 'BuzzFeed' },
    { key: 'polygon', text: 'Polygon', value: 'Polygon' },
    { key: 'espn', text: 'ESPN', value: 'ESPN' },

];

class Register extends Component {
    constructor() {
        super()
        this.state = {
            username: '',
            password: '',
            urls: []
        }

        this.onChange = this.onChange.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
    }

    onChange (e) {
        this.setState({ [e.target.name]: e.target.value })
    }

    handleDropDown = (event, data) => {
        console.log(data.value)
        this.setState({ urls: data.value })
    }

    onSubmit (e) {
        e.preventDefault()

        const newUser = {
            username: this.state.username,
            password: this.state.password,
            urls: this.state.urls
        }

        console.log(newUser);

        register(newUser).then(res => {
            this.props.history.push(`/login`)
        })
    }

    render () {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-md-6 mt-5 mx-auto">
                        <form noValidate onSubmit={this.onSubmit}>
                            <h1 className="h3 mb-3 font-weight-normal">Register</h1>
                            <div className="form-group">
                                <label htmlFor="username">Username </label>
                                <input type="username"
                                    className="form-control"
                                    name="username"
                                    placeholder="Enter Username"
                                    value={this.state.username}
                                    onChange={this.onChange} />
                            </div>
                            <div className="form-group">
                                <label htmlFor="password">Password </label>
                                <input type="password"
                                    className="form-control"
                                    name="password"
                                    placeholder="Enter Password"
                                    value={this.state.password}
                                    onChange={this.onChange} />
                            </div>
                            <div className="form-group">
                                <Dropdown placeholder='News Sources' 
                                        onChange={this.handleDropDown}
                                          fluid multiple selection options={data} />
                            </div>
                            <button type="submit" className="btn btn-lg btn-primary btn-block">
                                Register
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}

export default Register