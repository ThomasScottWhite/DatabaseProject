import React, { useState } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const CreateAccount = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [chapterID, setChapterID] = useState(0);
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [dob, setDob] = useState("");
  const [phoneNum, setPhoneNum] = useState("");

  const navigate = useNavigate();

  const formatPhoneNumber = (value) => {
    const digits = value.replace(/\D/g, "");

    const formatted = digits.replace(
      /^(\d{3})(\d{3})(\d{0,4}).*/,
      (_, p1, p2, p3) => `${p1}-${p2}-${p3}`.replace(/-$/, "")
    );

    return formatted;
  };

  const handlePhoneChange = (e) => {
    const formattedNumber = formatPhoneNumber(e.target.value);
    setPhoneNum(formattedNumber);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    const payload = {
      email: email,
      password: password,
      organization_info: {
        chapter_id: chapterID,
        fname: fname,
        lname: lname,
        dob: dob,
        phone_num: phoneNum,
      },
    };

    try {
      const response = await fetch("/api/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        alert("Account created successfully!");
        console.log("Server Response:", data);
        navigate("/"); // Redirect to home or login page
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail || "Account creation failed"}`);
      }
    } catch (error) {
      console.error("Error creating account:", error);
      alert("An error occurred while creating the account.");
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col xs={12} md={6}>
          <h2 className="text-center">Create New Account</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formEmail" className="mb-3">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formPassword" className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formConfirmPassword" className="mb-3">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formChapterID" className="mb-3">
              <Form.Label>Chapter ID</Form.Label>
              <Form.Control
                type="number"
                placeholder="Chapter ID"
                value={chapterID}
                onChange={(e) => setChapterID(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formFname" className="mb-3">
              <Form.Label>First Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="First Name"
                value={fname}
                onChange={(e) => setFname(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formLname" className="mb-3">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Last Name"
                value={lname}
                onChange={(e) => setLname(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formDob" className="mb-3">
              <Form.Label>Date of Birth</Form.Label>
              <Form.Control
                type="date"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formPhoneNum" className="mb-3">
              <Form.Label>Phone Number</Form.Label>
              <Form.Control
                type="text"
                placeholder="Phone Number (e.g., 888-888-8888)"
                value={phoneNum}
                onChange={handlePhoneChange}
                required
              />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100">
              Create Account
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default CreateAccount;
