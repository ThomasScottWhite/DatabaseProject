import React, { useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useUser } from '../context/user_context';

const MakeBills = () => {
    const [billName, setBillName] = useState('');
    const [amount, setAmount] = useState('');
    const [invoicee, setInvoicee] = useState('');
    const user = useUser();

    const make_bill_request = async (e) => {
        e.preventDefault();

        const payload = {
            bill_name: billName,
            invoicee_id: invoicee,
            amount: amount,
        };

        try {
            const response = await fetch('/api/make-bill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': user.auth_token,
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert("Bill Made")
            }

        } catch (error) {
            console.error('Error logging in:', error);
            alert('An error occurred while logging in.');
        }
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    <h2 className="text-center">Create a Bill</h2>
                    <Form onSubmit={make_bill_request}>
                        <Form.Group controlId="formBillName" className="mb-3">
                            <Form.Label>Bill Name</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Enter bill name"
                                value={billName}
                                onChange={(e) => setBillName(e.target.value)}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="formBillName" className="mb-3">
                            <Form.Label>Invoicee</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Enter account id"
                                value={invoicee}
                                onChange={(e) => setInvoicee(e.target.value)}
                                required
                            />
                        </Form.Group>

                        <Form.Group controlId="formAmount" className="mb-3">
                            <Form.Label>Amount</Form.Label>
                            <Form.Control
                                type="number"
                                placeholder="Enter amount"
                                value={amount}
                                onChange={(e) => setAmount(e.target.value)}
                                required
                            />
                        </Form.Group>

                        <Button variant="primary" type="submit" className="w-100">
                            Submit
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default MakeBills;
