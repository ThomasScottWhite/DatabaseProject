import React, { useState } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import { useUser } from "../context/user_context";

const PaymentScreen = () => {
  const user = useUser();
  const { id, amount, bill_name } = useParams();
  const [cardNumber, setCardNumber] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [cvv, setCvv] = useState("");
  const navigate = useNavigate();

  const handlePayment = async (e) => {
    e.preventDefault();

    const paymentData = {
      payment_amount: amount,
    };

    try {
      const response = await user.post_with_headers(
        `/api/bill/pay/${id}`,
        paymentData
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      alert(`Payment successful for ${bill_name}, amount: $${amount}`);
      navigate("/");
    } catch (error) {
      console.error("Payment failed:", error);
      alert("Payment failed. Please try again.");
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col xs={12} md={6}>
          <h2 className="text-center">Pay for {bill_name}</h2>
          <Form onSubmit={handlePayment}>
            <Form.Group controlId="formCardNumber" className="mb-3">
              <Form.Label>Card Number</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter card number"
                value={cardNumber}
                onChange={(e) => setCardNumber(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formExpiryDate" className="mb-3">
              <Form.Label>Expiry Date</Form.Label>
              <Form.Control
                type="text"
                placeholder="MM/YY"
                value={expiryDate}
                onChange={(e) => setExpiryDate(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formCvv" className="mb-3">
              <Form.Label>CVV</Form.Label>
              <Form.Control
                type="password"
                placeholder="CVV"
                value={cvv}
                onChange={(e) => setCvv(e.target.value)}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">
              Pay ${amount}
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default PaymentScreen;
