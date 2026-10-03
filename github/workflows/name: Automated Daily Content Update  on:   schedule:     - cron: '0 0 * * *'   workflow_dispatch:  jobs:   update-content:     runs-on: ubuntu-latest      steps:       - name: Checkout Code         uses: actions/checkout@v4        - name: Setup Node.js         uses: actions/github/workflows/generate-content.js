import { GoogleGenAI } from '@google/genai';
import fs from 'fs';
import path from 'path';

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  console.error("Error: GEMINI_API_KEY missing!");
  process.exit(1);
}

const ai = new GoogleGenAI({ apiKey });

async function generateDailyContent() {
  console.log("Generating daily content...");

  const prompt = `
Generate 3 viral content ideas for content creators across different niches (e.g., Tech & Gadgets, Finance & Business).
Return ONLY a valid JSON array of objects with no markdown code blocks.

Exact structure required for each item:
{
  "id": "${Date.now()}",
  "title": "Catchy Hook / Title",
  "niche": "tech",
  "description": "Brief explanation of content idea",
  "viralScore": "95%",
  "tags": ["Tag1", "Tag2"],
  "status": "approved",
  "createdAt": "${new Date().toISOString().split('T')[0]}"
}
`;

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });

    let rawText = response.text.trim().replace(/```json/g, '').replace(/```/g, '').trim();
    const newItems = JSON.parse(rawText);

    const filePath = path.join(process.cwd(), 'data', 'content.json');
    let existingData = [];

    if (fs.existsSync(filePath)) {
      try {
        existingData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      } catch (e) {
        existingData = [];
      }
    } else {
      fs.mkdirSync(path.join(process.cwd(), 'data'), { recursive: true });
    }

    const updatedData = [...newItems, ...existingData].slice(0, 50);
    fs.writeFileSync(filePath, JSON.stringify(updatedData, null, 2), 'utf-8');
    console.log("Content updated successfully!");
  } catch (error) {
    console.error("Failed to generate content:", error);
    process.exit(1);
  }
}

generateDailyContent();
