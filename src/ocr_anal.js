import { OpenAI } from "openai";

const fs = require("fs");


// This JavaScript code replicates the logic of the provided Python code. 
// It doesn't cover all functionalities (such as image processing) due to differences in libraries and handling in JavaScript.

// A dictionary to represent the STORE_DICT in Python
const STORE_DICT = {
    "rema 1000": { startText: "serienr", endText: "sum " },
    "coop obs": { startText: "ref", endText: "totalt " },
    "coop extra": { startText: "salgskvittering", endText: "totalt " },
    "unknown": { startText: "unknown", endText: "unknown " }
  };
  
  function exportImageText(imagePath) {
    // Simulating the pytesseract.image_to_string function in Python
    // Image processing is highly specific and complex, not covered here
    return "Simulated image text from " + imagePath;
  }
  
  function makeGPTRequest(imagePath) {
    const messagePrefix =
      "Lag et JSON-datasett fra følgende matvarer. Svaret skal være på formatet {'matvare': {'antall': int, 'vekt': str, 'kategori': str}, ...}. Defaultverdi for antall skal være 1, vekt skal være 'N/A' og kategori skal være innenfor kjøleskap, tørrvare eller fryser. Rett opp i skrivefeil og generaliser navnet på matvaren.";
  
    const prompt = makeGPTPrompt(imagePath);
    // Simulating API call or GPT-3 usage for JavaScript, result variable is assumed here
    const result = simulateGPTResponse(prompt);
  
    dumpGPTRequest(result);
  }
  
  function makeGPTPrompt(imagePath) {
    const lines = exportImageText(imagePath).split("\n");
    let store = lines[0].toLowerCase();
  
    if (store.includes("extra")) {
      store = "coop extra";
    } else if (store.includes("obs")) {
      store = "coop obs";
    } else if (store.includes("rema")) {
      store = "rema 1000";
    } else {
      store = "unknown";
    }
  
    store = STORE_DICT[store];
  
    let startIdx = 0;
    let endIdx = lines.length;
  
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (!startIdx && line.startsWith(store.startText)) {
        startIdx = i + 1;
      } else if (line.startsWith(store.endText)) {
        endIdx = i;
        break;
      }
    }
  
    const result = [];
    for (let i = startIdx; i < endIdx; i++) {
      if (!lines[i].startsWith("pant")) {
        result.push(lines[i]);
      }
    }
  
    return result.join(", ");
  }
  
  async function simulateGPTResponse(prompt) {

    // Simulating the GPT-3 API response in JavaScript
    const openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY,
    });
    const chatCompletion = await openai.chat.completions.create({
        messages: [{ role: "user", content: "Lag et JSON-datasett fra følgende matvarer. Svaret skal være på formatet {'matvare': {'antall': int, 'vekt': str, 'kategori': str}, ...}. Defaultverdi for antall skal være 1, vekt skal være 'N/A' og kategori skal være innenfor kjøleskap, tørrvare eller fryser. Rett opp i skrivefeil og generaliser navnet på matvaren.:\n, battery brry 0 5l bx 25.90, , xtra grillpølse 1kg 33.40, , xtra kneippbrød 10.90, , xtra pizzatopping 47.00," }],
        model: "gpt-3.5-turbo",
    });
    console.log(chatCompletion);
    // Process the response, transform or convert as required
    // const processedResult = JSON.parse(simulatedResponse.replace(/'/g, '"'));
    // return processedResult;
  }
  
  // Execution - call the function with an image path
  const imagePath = "src/receipts/rema_1000.jpg";
  makeGPTRequest(imagePath);
  