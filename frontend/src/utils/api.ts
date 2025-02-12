const API_BASE_URL = "http://localhost:5000"; // Ensure this matches your backend port

export const fetchData = async (): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/data`);
    if (!response.ok) throw new Error("Failed to fetch data");
    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
};