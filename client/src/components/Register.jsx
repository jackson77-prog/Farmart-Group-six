import React from 'react';
import './Register.css';

const Register = () => {
    return (
        <div className="register">
            <h2>Register</h2>
            <form>
                <label>
                    Account Type:
                    <select>
                        <option value="farmer">Farmer</option>
                        <option value="buyer">Buyer</option>
                    </select>
                </label>
                <label>
                    Full Name:
                    <input type="text" name="fullname" />
                </label>
                <label>
                    Email:
                    <input type="email" name="email" />
                </label>
                <label>
                    Telephone:
                    <input type="tel" name="telephone" />
                </label>
                <label>
                    County:
                    <input type="text" name="county" />
                </label>
                <label>
                    Town:
                    <input type="text" name="town" />
                </label>
                <label>
                    Password:
                    <input type="password" name="password" />
                </label>
                <label>
                    Confirm Password:
                    <input type="password" name="confirm_password" />
                </label>
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;
