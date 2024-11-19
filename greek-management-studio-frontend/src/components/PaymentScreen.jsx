import React, { useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import { useUser } from '../context/user_context';

const PaymentScreen = () => {
    const [cardNumber, setCardNumber] = useState('');
    const [expiryDate, setExpiryDate] = useState('');
    const [cvv, setCvv] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const { bill } = location.state; // Passed from ViewBills

    const handlePayment = (e) => {
        e.preventDefault();
        console.log(`Paid for Bill: ${bill.name}, Amount: ${bill.amount}`);

        // Here, you would typically send the payment data to the server

        // Simulate payment processing and redirect back to View Bills after payment
        alert(`Payment of $${bill.amount} for ${bill.name} completed!`);
        navigate('/'); // Redirect back to the main page
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    <h2 className="text-center">Pay for {bill.name}</h2>
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
                            Pay ${bill.amount}
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default PaymentScreen;
