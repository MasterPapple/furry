const {Client, IntentsBitField, EmbedBuilder} = require('discord.js');
const net = require('net');
const fs = require('fs');
const imgur = require('imgur')
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
var image_list = {};
var messages_list = JSON.parse(fs.readFileSync("src/messages.json"))

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
    console.log(data.toString())
    const split_data = data.toString().split("%");
    if (split_data[0] == "furry_attack") {

        var furryEmbedString = fs.readFileSync("src/fight.json").toString();   
        furryEmbedString = furryEmbedString
            .replace("$health", split_data[3])
            .replaceAll("$name", split_data[1])
            .replace("$strength", split_data[2])
            .replace("$hero_health", split_data[4])
            .replace("$actions", split_data[5])
            .replace("$hero_strength", split_data[6])
            .replace("$weapon_name", split_data[7])
            .replace("$damage", split_data[8])
            .replace("$breed", split_data[9]);

        if (image_list[split_data[1]] !== undefined){
            furryEmbedString = furryEmbedString.replace('$url', image_list[split_data[1]]);
        } else {
            furryEmbedString = furryEmbedString.replace('$url', "https://storage.googleapis.com/proudcity/mebanenc/uploads/2021/03/placeholder-image.png");
        }
    
        var embed = JSON.parse(furryEmbedString);
        current_channel.send({ embeds: [embed] });
    } else {


        embed = embedBuilding(split_data[0], split_data)
        if (embed === false && current_channel != null){

            const exampleEmbed = new EmbedBuilder()
                .setColor(0x0099FF)
                .setDescription(`${data}`);
            current_channel.send({embeds: [exampleEmbed]});
        }
        else {
            if (split_data[0] == 'furry_spawn') {
                uploadImage(split_data[2], split_data[1])
            }
            if (split_data[0] == 'tech_tree') {
                imgur.uploadFile('tech_images/image.png').then((urlObject) => {
                    console.log(urlObject.link)
                    embed['image'] = {url: urlObject.link.toString()}
                    current_channel.send({embeds: [embed]});
                })
            } else {
                current_channel.send({embeds: [embed]});
            }
        }
    }


    
});


function embedBuilding(task, data_list) {
    if (messages_list[task] === undefined) {
        return false
    }
    var embed_helper = JSON.stringify(messages_list[task])
    for (element in data_list) {
        var data_string = '$data' + element.toString()
        console.log(data_string)
        console.log(data_list[element])
        embed_helper = embed_helper.replaceAll(data_string, data_list[element])
    }
    embed_helper = JSON.parse(embed_helper)
    const add_actions = embed_helper['append_actions']
    delete embed_helper.append_actions
    if (add_actions) {
        const last = data_list.slice(-1)
        embed_helper['footer'] = {text: `Available actions include ${last}`}
    }

    return embed_helper
}

function uploadImage(uploadPath, name) {
    imgur.uploadFile(uploadPath).then((urlObject) => {
        image_list[name] = urlObject.link.toString();
        console.log(urlObject.link)
        return urlObject.link.toString()
    })
}


connection.on('close', () => {
    console.log('Connection closed!');
})


/*else if (embedSender(split_data, 'furry_spawn', 0xDD0007, `Your virginity is at risk! Defeat the ${split_data[2]}!`, true)) {
    uploadImage(split_data[3], split_data[2])
}
else if (split_data[0] == 'merchant' && split_data[2] == 'None') {
    embedSender(split_data, 'merchant', 0xE008B1, 'You encountered a merchant.', true)
} else if (embedSender(split_data, 'merchant', 0xE008B1, `You encountered a merchant and he has a crazy offer for ${split_data[2]}`, true)) {}
else if (embedSender(split_data, 'inn_walk', 0xE2E231, 'You wallked by an inn and feel a bit weary', true)) {}
else if (embedSender(split_data, 'furry_kill', 0x818EEF, 'You completely abused the Furry, till he unalived!')) {}
else if (embedSender(split_data, 'rest', 0x06AD09, `You rested well and healed for ${split_data[1]}.`)) {}
else if (embedSender(split_data, 'purchase', 0x06AD09, `You successfully bought ${split_data[1]} and it has become your new weapon of choice!`)) {}
else if (embedSender(split_data, 'tech_tree', 0x800080, `You have currently ${split_data[1]} skill points available!`, false, 'tech')) {}*/
