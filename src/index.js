const {Client, IntentsBitField, EmbedBuilder} = require('discord.js');
const net = require('net');
const fs = require('fs');
require('dotenv').config();

const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMembers,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
        IntentsBitField.Flags.GuildMessageTyping,

    ],
});

var current_channel = null;

client.on('ready', (c) => {
    console.log(`${c.user.tag} is online`)
});

var receive_prefixless = false;

client.on('messageCreate', (message) => {
    if (message.author.id === client.user.id) return;
    if (message.content.startsWith('>')) {
        current_channel = message.channel;
        connection.write(`${message.author.id}%${message.content.slice(1)}`);
    }
    if (receive_prefixless) {
        connection.write(`${message.content}%${message.author.id}`);
        receive_prefixless = false;
    }
});

client.login(process.env.TOKEN);


const connection = new net.Socket();

connection.connect(8080, '192.168.1.27', () => {
    console.log(`Connected to python server`);
});

connection.on('data', (data) => {
    if (current_channel == null) return;
    if (`${data}` == "What's your name?") {
        receive_prefixless = true;
    }
    const split_data = data.toString().split("%");
    if (split_data[0] == "furry_attack") {

        var furryEmbedString = fs.readFileSync("src/fight.json").toString();   
        furryEmbedString = furryEmbedString
            .replace("$health", split_data[3])
            .replace("$name", split_data[1])
            .replace("$strength", split_data[2])
            .replace("$hero_health", split_data[4])
            .replace("$actions", split_data[5]);
    
        var embed = JSON.parse(furryEmbedString);
        current_channel.send({ embeds: [embed] });
    }
    else if (embedSender(split_data, 'furry_spawn', 0xDD0007, `Your virginity is at risk! Defeat the ${split_data[2]}!`, true)) {}
    else if (embedSender(split_data, 'merchant', 0xE008B1, 'You encountered a merchant.', true)) {}
    else if (embedSender(split_data, 'inn_walk', 0xE2E231, 'You wallked by an inn and feel a bit weary', true)) {}
    else if (embedSender(split_data, 'furry_kill', 0x818EEF, 'You completely abused the Furry, till he unalived!')) {}
    else if (embedSender(split_data, 'rest', 0x06AD09, `You rested well and healed for ${split_data[1]}.`)) {}
    else if (embedSender(split_data, 'purchase', 0x06AD09, `You successfully bought ${split_data[1]} and it has become your new weapon of choice!`)) {}

    else if (current_channel != null) {
        const exampleEmbed = new EmbedBuilder()
            .setColor(0x0099FF)
            .setDescription(`${data}`);
        current_channel.send({embeds: [exampleEmbed]});  
    }
});

function embedSender(split_data, action_name, color, description, add_action = false) {
    if (split_data[0] == action_name) {
        var embed = new EmbedBuilder()
            .setColor(color)
            .setDescription(description);
        if (add_action) {
            embed.setFooter({text: `Available actions include ${split_data[1]}`});
        }       
        current_channel.send({embeds: [embed]});
        return true
    }
}

connection.on('close', () => {
    console.log('Connection closed!');
} )