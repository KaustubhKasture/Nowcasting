const quizdata = [
{
    question: 'How old is Vanshika?',
    a : '20',
    b : '21',
    c : '23',
    d : '22',
    correct: 'b'
}, {
    question: 'Most used pg language?',
    a : 'Python',
    b : 'C',
    c : 'Java',
    d : 'JS',
    correct: 'c'
}, {
    question: 'what is my job?',
    a : 'student',
    b : 'SDE',
    c : 'Web devp',
    d : 'Marketer',
    correct: 'a'
}, {
    question: 'Class is a blueprint of?',
    a : 'Abstraction',
    b : 'Polymorphsim',
    c : 'OOP',
    d : 'Class',
    correct: 'd'
}


];

const questionE1 = document.getElementById('question');
const a_txt  =  document.getElementById('a_txt');
const b_txt = document.getElementById('b_txt');
const c_txt = document.getElementById('c_txt');
const d_txt = document.getElementById('d_txt');


let currentques = 0;

loadQuiz();

function loadQuiz() {
    const currentques = quizdata[currentques];
 
    questionE1.innerHTML = currentquizdata.question;

    a_txt.innerText = currentquizdata.a;
    b_txt.innerText = currentquizdata.b;
    c_txt.innerText = currentquizdata.c;
    d_txt.innerText = currentquizdata.d;
    

    currentques++;
}