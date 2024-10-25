import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(`Email: ${email}, Password: ${password}`);
        // Assuming the user logs in successfully, navigate to the Members page
        navigate('/MainPage');
    };

    return (
        <Container className="d-flex justify-content-center align-items-center min-vh-100">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    <h2 className="text-center mb-4">Login</h2>
                    <Form onSubmit={handleSubmit}>
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
