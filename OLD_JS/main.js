const { NseIndia } = require("stock-nse-india");

const nseIndia = new NseIndia();

// Get all stock symbols from NSE
nseIndia.getAllStockSymbols().then(symbols => {
    console.log(symbols);
});

// Get equity details for a specific stock
nseIndia.getEquityDetails("IR").then(details => {
    console.log(details);
});

// Get historical data for a stock
const range = {
    start: new Date("2024-01-01"),
    end: new Date("2025-03-20")
};

nseIndia.getEquityHistoricalData("TRENT", range).then(data => {
    console.log(data);
});
// const { NseIndia } = require("stock-nse-india");

// const nseIndia = new NseIndia();

// nseIndia.getIndices().then(data => {
//     const niftyData = data.find(index => index.index === "NIFTY 50");
//     console.log("NIFTY 50 Data:", niftyData);
// }).catch(err => {
//     console.error("Error fetching NIFTY 50 data:", err);
// });
