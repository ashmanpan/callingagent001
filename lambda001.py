// Lambda function
const { BedrockAgentRuntimeClient, InvokeAgentCommand } = require("@aws-sdk/client-bedrock-agent-runtime");

exports.handler = async (event) => {
    const client = new BedrockAgentRuntimeClient({ region: "us-east-1" });
    
    try {
        const prompt = JSON.parse(event.body).prompt;
        
        const command = new InvokeAgentCommand({
            agentId: "KFXQCOCU86",
            agentAliasId: "LATEST",
            sessionId: Date.now().toString(),
            inputText: prompt
        });

        const response = await client.send(command);
        let completion = "";

        for await (const chunkEvent of response.completion) {
            const chunk = chunkEvent.chunk;
            const decodedResponse = new TextDecoder("utf-8").decode(chunk.bytes);
            completion += decodedResponse;
        }

        return {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin": "*", // Configure this appropriately
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ completion })
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers: {
                "Access-Control-Allow-Origin": "*", // Configure this appropriately
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ error: error.message })
        };
    }
};
