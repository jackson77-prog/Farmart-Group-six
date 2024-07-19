import React from 'react';
import './Login.css';

const Login = () => {
    return (
        <div className="login">
            <h2>Login</h2>
            <form>
                <label>
                    Account Type:
                    <select>
                        <option value="farmer">Farmer</option>
                        <option value="buyer">Buyer</option>
                    </select>
                </label>
                <label>
                    Email:
                    <input type="email" name="email" />
                </label>
                <label>
                    Password:
                    <input type="password" name="password" />
                </label>
                <button type="submit">Login</button>
            </form>
            <a href="/forgot-password" className="forgot-password">Forgot Password?</a>
        </div>
    );
};

export default Login;
