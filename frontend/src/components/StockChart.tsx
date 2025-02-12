import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { date: "2025-02-10", price: 150 },
    { date: "2025-02-11", price: 155 },
    { date: "2025-02-12", price: 160 },
];

const StockChart: React.FC = () => {
    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="price" stroke="#8884d8" />
            </LineChart>
        </ResponsiveContainer>
    );
};

export default StockChart;