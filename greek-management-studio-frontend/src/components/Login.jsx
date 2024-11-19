import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/user_context';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const user = useUser();

    const login_request = async (e) => {
        e.preventDefault();

        const payload = {
            username: email,
            password: password,
        };

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                const data = await response.json();
                // Use user context to update login state
                user.login(email, data.organization_id, data.account_id, data.auth_token);
                navigate('/mainpage');
            } else {
                // Handle login failure (example: setting test data)
                user.login('test@gmail.com', '1', '1');
                navigate('/mainpage');
            }
        } catch (error) {
            console.error('Error logging in:', error);
            alert('An error occurred while logging in.');
        }
    };

    return (
        <Container className="d-flex justify-content-center align-items-center min-vh-100">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    <h2 className="text-center mb-4">Login</h2>
                    <Form onSubmit={login_request}>
                        <Form.Group controlId="formBasicEmail" className="mb-3">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control
                                type="email"
                                placeholder="Enter email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </Form.Group>

                        <Form.Group controlId="formBasicPassword" className="mb-3">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </Form.Group>

                        <Button variant="primary" type="submit" className="w-100">
                            Submit
                        </Button>

                    </Form>

                    <Row className="mt-4">
                        <h2 className="text-center mt-4 mb-4">Create New Accounts</h2>

                        <Col className="text-center">
                            <Link to="/create-account">
                                <Button variant="primary" className="w-100 mb-2">
                                    Create New Account
                                </Button>
                            </Link>

                            <Link to="/create-organization">
                                <Button variant="secondary" className="w-100">
                                    Create New Organization
                                </Button>
                            </Link>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
    );
};

export default Login;
