// SignupForm.js
import React, { useState } from 'react';
import axios from 'axios';

const SignupForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });

    const handleChange = e => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async e => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/signup/', formData);
            console.log(res.data);
        } catch (error) {
            console.error(error.response.data);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} />
            <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} />
            <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} />
            <button type="submit">Sign Up</button>
        </form>
    );
};

export default SignupForm;
