import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/user_context";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const user = useUser();

  const login_request = async (e) => {
    e.preventDefault();

    const payload = {
      email: email,
      password: password,
    };

    try {
      const response = await fetch("/api/user/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Login response data:", data);

        user.login(
          data.chapter_id,
          data.auth_token,
          data.email,
          data.is_chapter_admin,
          () => {
            console.log("State updated. Navigating...");
            navigate("/mainpage");
          }
        );
      } else {
        console.error("Login failed. Response not OK.");
        alert("Invalid credentials. Please try again.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("An error occurred while logging in. Please try again.");
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
            <h2 className="text-center mt-4 mb-4">Create New Account</h2>

            <Col className="text-center">
              <Link to="/create-account">
                <Button variant="primary" className="w-100 mb-2">
                  Create New Account
                </Button>
              </Link>

              {/* <Link to="/create-organization">
                <Button variant="secondary" className="w-100">
                  Create New Organization
                </Button>
              </Link> */}
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default Login;
