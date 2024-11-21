import React, { useState, useEffect } from "react";
import { Table, Container, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/user_context";

const ViewBills = () => {
  const [bills, setBills] = useState([
    {
      invoicee_id: 1,
      bill_name: "Chapter Rent",
      amount: 1000,
      date: "2024-10-30",
      invoicee_name: "Joe",
      paid: "Unpaid",
      bill_id: 1,
    },
    {
      invoicee_id: 2,
      bill_name: "Greek Markup",
      amount: 500,
      date: "2024-11-05",
      invoicee_name: "Joe",
      paid: "Unpaid",
      bill_id: 2,
    },
    {
      invoicee_id: 3,
      bill_name: "Parking (we are evil)",
      amount: 30,
      date: "2024-10-28",
      invoicee_name: "Joe",
      paid: "Unpaid",
      bill_id: 3,
    },
  ]);
  const payload = { someKey: "someValue" };
  const user = useUser();
  const Refresh = async () => {
    try {
      const response = await user.get_with_headers("/api/my-bills");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setBills(data.bills);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    Refresh();
  }, []);

  const navigate = useNavigate();

  const handlePay = (bill) => {
    navigate(`/payment/${bill.bill_id}/${bill.amount}/${bill.bill_name}`);
  };

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">View Bills</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Bill Id</th>
            <th>Bill Name</th>
            <th>Amount ($)</th>
            <th>Due Date</th>
            <th>Source</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {bills.map((bill) => (
            <tr key={bill.invoicee_id}>
              <td>{bill.invoicee_id}</td>
              <td>{bill.bill_id}</td>
              <td>{bill.bill_name}</td>
              <td>{bill.amount}</td>
              <td>{bill.date}</td>
              <td>{bill.invoicee_name}</td>
              <td>{bill.paid ? "Paid" : "Unpaid"}</td>
              <td>
                {!bill.paid ? (
                  <Button variant="success" onClick={() => handlePay(bill)}>
                    Pay
                  </Button>
                ) : (
                  "Paid"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default ViewBills;
