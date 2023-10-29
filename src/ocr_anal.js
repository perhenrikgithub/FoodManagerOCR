import { OpenAI } from "openai";

// const fs = require("fs");

const STORE_DICT = {
    "rema 1000": { startText: "serienr", endText: "sum " },
    "coop obs": { startText: "ref", endText: "totalt " },
    "coop extra": { startText: "salgskvittering", endText: "totalt " },
    "unknown": { startText: "unknown", endText: "unknown " }
};
  
function exportImageText(imagePath) {
    // TODO: Replace with actual image processing (KASPER)
    const completeImagePath = "src/receipts/" + imagePath;
    return "Simulated image text from " + imagePath;
}
  
async function makeGPTRequest(imagePath) {
    // const prompt = makeGPTPrompt(imagePath);
    const prompt = "battery brry 0 5l bx 25.90, , xtra grillpølse 1kg 33.40, , xtra kneippbrød 10.90, , xtra pizzatopping 47.00,";
    
    const messagePrefix = "Lag et JSON-datasett fra følgende matvarer. Svaret skal være på formatet {'matvare': {'antall': int, 'vekt': str, 'kategori': str}, ...}. Defaultverdi for antall skal være 1, vekt skal være 'N/A' og kategori skal være innenfor kjøleskap, tørrvare eller fryser. Rett opp i skrivefeil og generaliser navnet på matvaren:\n";
    
    // TODO: Replace with actual apiKey, using .env file
    const openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY
    });

    const chatCompletion = await openai.chat.completions.create({
        messages: [{ role: "user", content: messagePrefix + prompt }],
        model: "gpt-3.5-turbo",
        temperature: 0.0,
    });
    // console.log(chatCompletion);
    
    // TODO: Verify that the result has the correct format
    const result = chatCompletion.choices[0].message.content;
    // console.log(result);

    const processedResult = JSON.parse(result.replace(/'/g, '"'));
    return processedResult;
}

function makeGPTPrompt(imagePath) {
    const lines = exportImageText(imagePath).toLowerCase().split("\n");
    let store = lines[0];
    
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

const imagePath = "rema_1000.jpg";
makeGPTRequest(imagePath);
