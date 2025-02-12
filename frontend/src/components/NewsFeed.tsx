import React, { useEffect, useState } from "react";

const NewsFeed: React.FC = () => {
    const [news, setNews] = useState<string[]>([]);

    useEffect(() => {
        fetch("/api/stocks/news")
            .then((res) => res.json())
            .then((data) => setNews(data.articles));
    }, []);

    return (
        <div className="border p-4">
            <h2 className="text-xl font-bold">Stock News</h2>
            <ul>
                {news.map((article, index) => (
                    <li key={index} className="text-sm mt-2">{article}</li>
                ))}
            </ul>
        </div>
    );
};

export default NewsFeed;