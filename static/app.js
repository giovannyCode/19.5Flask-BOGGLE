const BASE_URL = "http://127.0.0.1:5000/";
class BoogleGame {

  constructor ()
  {
      this.score = 0;
      this.usedWords =[];
      this.maxScore = 0 ;
      this.timesPlayed = 0;
  }
  
  increaseScore (word)
  {
    this.score =  this.score + word.length
    
  }

  isinUsedWords(word)
  {
     if (this.usedWords.indexOf(word) > -1)
     {
      return true;
     }
     else
     { 
      return false
      }
  }

  async statistics ()
  {
    const response = await axios({
      method: 'post',
      url: `${BASE_URL}/statistics`,
      data: {
             currentScore:this.score,
          }
    });
    this.maxScore = response.data.maxScore;
    this.timesPlayed = response.data.timesPlayed;

  }
  
}
const game = new BoogleGame();
async function runStatistics()
{
  await game.statistics();
  printstadistics();
} 
runStatistics();
startCountdown();
console.log(game.score); 




document.getElementById("letterform").addEventListener("submit",validateWord) ;

async function validateWord(evt) {
  evt.preventDefault();
  console.log("I am in validateWord");
  let wordForm  = document.getElementById("inputWord").value;
  console.log(wordForm);
  if (game.isinUsedWords(wordForm))
  { 
    showMessage("Word already played","error");
  }
  else
  {
    const response = await axios({
      method: 'post',
      url: `${BASE_URL}/validateWord`,
      data: {
        word:wordForm 
        }
    });
     const {result} = response.data
     if(result == 'ok')
     {
        game.increaseScore(wordForm);
        document.getElementById("score").innerText = game.score;
        document.getElementById("inputWord").value = "";
  
        showMessage(result,"success")
        game.usedWords.push(wordForm);
     }
    else
    {
      showMessage(result,"error");
      document.getElementById("inputWord").value = "";
    }
    
  }
}

function  showMessage ( message, classtype)
{
  document.getElementById("boggleMessage").className ='';
  document.getElementById("boggleMessage").classList.add("messages");
  document.getElementById("boggleMessage").classList.add(classtype);
  document.getElementById("boggleMessage").innerText = message; 

}
function startCountdown() {
  const countdownElement = document.getElementById('boggleCounter');
  const endTime = Date.now() + 60000; // Set the end time (60 seconds from now)

  async function updateCountdown() {
    const currentTime = Date.now();
    const timeRemaining = endTime - currentTime;

    if (timeRemaining <= 0) {
      countdownElement.innerHTML = 'Time is up!';
      await game.statistics();
      printstadistics();
      document.getElementById("submitWord").hidden = true;
    } else {
      const secondsRemaining = Math.ceil(timeRemaining / 1000);
      countdownElement.innerHTML = secondsRemaining;
      setTimeout(updateCountdown, 1000); // Update the countdown every second
    }
  }

  updateCountdown();
}

function  printstadistics()
{
   let maxScore = game.maxScore;
   let  timesPlayed = game.timesPlayed;
   document.getElementById("stadistics").innerText = "";
  document.getElementById("stadistics").innerText = `Max score: ${maxScore} times played: ${timesPlayed}`;
}