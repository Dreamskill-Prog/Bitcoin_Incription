const SERVER_ADDRESS = process.env.NODE_ENV === "production" 
  ? "http://146.118.70.33" // Value for production build
  : "http://localhost:8000"; // Value for development
export { SERVER_ADDRESS };

export const NFT_COST = '0.0001' 