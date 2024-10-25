import React, { useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';

const MakeBills = () => {
    const [billName, setBillName] = useState('');
    const [amount, setAmount] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(`Bill Name: ${billName}, Amount: ${amount}`);
        // Handle bill creation logic here
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    <h2 className="text-center">Create a Bill</h2>
                    <Form onSubmit={handleSubmit}>
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
                                value={billName}
                                onChange={(e) => setBillName(e.target.value)}
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
