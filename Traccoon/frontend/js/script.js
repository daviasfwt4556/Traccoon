// ==========================================
// SPA - TROCA DE TELAS E ANIMAÇÕES
// ==========================================
function navigateTo(screenId) {
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => screen.classList.remove('active'));

    const activeScreen = document.getElementById(screenId);
    if (activeScreen) {
        activeScreen.classList.add('active');
    }

    if (screenId === 'screen-trails') animarBarrasDeProgresso();
    if (screenId === 'screen-result') gerarConfetes();
    if (screenId === 'screen-historico' && typeof carregarHistorico === 'function') {
        carregarHistorico();
    }
}

// ==========================================
// MODO ESCURO (SWITCH)
// ==========================================
const themeSwitch = document.getElementById('theme-toggle-switch');
const savedTheme = localStorage.getItem('autotran-theme');

if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark' && themeSwitch) themeSwitch.checked = true;
}

if (themeSwitch) {
    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('autotran-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('autotran-theme', 'light');
        }
    });
}

// ==========================================
// LÓGICA DINÂMICA DO QUIZ (1 A 10)
// ==========================================

const quizData = [
    { pergunta: "O que significa a placa de advertência com o desenho de um semáforo?", opcoes: ["Parada Obrigatória à frente", "Semáforo à frente", "Dê a preferência", "Trânsito impedido"], correta: 1 },
    { pergunta: "A placa 'R-1' (Pare) é de formato octogonal com fundo vermelho. O que o condutor deve fazer ao avistá-la?", opcoes: ["Reduzir a velocidade", "Parar o veículo obrigatoriamente", "Buzinar", "Dar preferência apenas a pedestres"], correta: 1 },
    { pergunta: "Qual a cor predominante da placa que indica 'Obras' (A-24)?", opcoes: ["Amarela", "Laranja", "Vermelha", "Azul"], correta: 1 },
    { pergunta: "A placa de regulamentação 'R-33' (Seta em círculo) indica:", opcoes: ["Parada obrigatória", "Proibido virar à esquerda", "Movimento circular obrigatório na rotatória", "Trânsito de bicicletas"], correta: 2 },
    { pergunta: "Qual a finalidade das placas de Regulamentação?", opcoes: ["Alertar sobre perigos na via", "Indicar direções e distâncias", "Informar proibições, obrigações ou restrições", "Educar os pedestres"], correta: 2 },
    { pergunta: "A placa 'R-6a' (círculo vermelho com um corte diagonal) significa:", opcoes: ["Proibido Estacionar", "Proibido Parar e Estacionar", "Estacionamento Regulamentado", "Área de Carga e Descarga"], correta: 0 },
    { pergunta: "A placa 'A-15' adverte o condutor da existência, adiante, de:", opcoes: ["Há obras na via", "Estreitamento de pista ao centro", "A pista passará a ter mão dupla", "Ponte estreita"], correta: 1 },
    { pergunta: "As placas de Indicação têm a função de:", opcoes: ["Ditar regras de trânsito", "Alertar sobre perigos", "Orientar sobre destinos, distâncias e serviços", "Multar infratores"], correta: 2 },
    { pergunta: "A placa de regulamentação 'R-24a' (Seta apontando para a direita) indica:", opcoes: ["Sentido duplo", "Sentido obrigatório", "Passagem obrigatória", "Siga em frente ou à direita"], correta: 1 },
    { pergunta: "A placa 'A-21a' adverte o condutor sobre o que à frente?", opcoes: ["Estreitamento de pista à esquerda", "Estreitamento de pista à direita", "Alargamento de pista à esquerda", "Deslizamento de terra"], correta: 0 }
];

let questaoAtualIndex = 0;
let opcaoSelecionada = null;
let acertos = 0;

function iniciarQuiz() {
    questaoAtualIndex = 0;
    acertos = 0;
    carregarQuestao();
    navigateTo('screen-quiz');
}

function carregarQuestao() {
    opcaoSelecionada = null;
    const q = quizData[questaoAtualIndex];

    document.getElementById('quiz-contador').textContent = `Questão ${questaoAtualIndex + 1}/10`;
    document.getElementById('quiz-pergunta').textContent = q.pergunta;

    const letras = ['A) ', 'B) ', 'C) ', 'D) '];
    for (let i = 0; i < 4; i++) {
        const btn = document.getElementById(`btn-op-${i}`);
        btn.textContent = letras[i] + q.opcoes[i];
        btn.className = 'quiz-option';
    }

    const btnConfirmar = document.getElementById('btn-confirmar');
    btnConfirmar.textContent = 'Confirmar Resposta';
    btnConfirmar.onclick = confirmarResposta;
}

function selecionarOpcao(index) {
    const btnConfirmarText = document.getElementById('btn-confirmar').textContent;
    if (btnConfirmarText === 'Próxima Questão' || btnConfirmarText === 'Ver Resultados') return;

    opcaoSelecionada = index;
    for (let i = 0; i < 4; i++) document.getElementById(`btn-op-${i}`).classList.remove('selected');
    document.getElementById(`btn-op-${index}`).classList.add('selected');
}

function confirmarResposta() {
    if (opcaoSelecionada === null) { alert('Selecione uma alternativa antes de confirmar!'); return; }

    const q = quizData[questaoAtualIndex];
    const btnClicado = document.getElementById(`btn-op-${opcaoSelecionada}`);

    if (opcaoSelecionada === q.correta) {
        btnClicado.classList.add('selected');
        btnClicado.classList.remove('error');
        acertos++;
    } else {
        btnClicado.classList.add('error');
        btnClicado.classList.remove('selected');
        document.getElementById(`btn-op-${q.correta}`).classList.add('selected');
    }

    const btnConfirmar = document.getElementById('btn-confirmar');
    if (questaoAtualIndex === quizData.length - 1) {
        btnConfirmar.textContent = 'Ver Resultados';
        btnConfirmar.onclick = finalizarQuiz;
    } else {
        btnConfirmar.textContent = 'Próxima Questão';
        btnConfirmar.onclick = () => { questaoAtualIndex++; carregarQuestao(); };
    }
}

function finalizarQuiz() {
    document.getElementById('resultado-acertos').textContent = `${acertos}/10`;
    const totalXP = acertos * 15;
    document.getElementById('resultado-xp').textContent = `+${totalXP}`;
    navigateTo('screen-result');
}

// ==========================================
// ANIMAÇÃO: BARRAS DE PROGRESSO
// ==========================================
function animarBarrasDeProgresso() {
    const barras = document.querySelectorAll('.progress-fill');
    barras.forEach(b => { b.style.width = '0%'; });
    setTimeout(() => {
        barras.forEach(b => { b.style.width = b.dataset.progresso || '0%'; });
    }, 100);
}

// ==========================================
// ANIMAÇÃO: CHUVA DE CONFETES
// ==========================================
function gerarConfetes() {
    const container = document.getElementById('screen-result');
    const colors = ['#38a169', '#ecc94b', '#e53e3e', '#3182ce', '#805ad5'];
    for (let i = 0; i < 40; i++) {
        let confete = document.createElement('div');
        confete.classList.add('confetti');
        confete.style.left = Math.random() * 100 + '%';
        confete.style.animationDuration = (Math.random() * 3 + 2) + 's';
        confete.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        container.appendChild(confete);
        setTimeout(() => confete.remove(), 5000);
    }
}

// ==========================================
// FLASHCARD 3D
// ==========================================
function virarCard(cardElement) {
    cardElement.classList.toggle('flipped');
}

function proximoCard() {
    const card = document.querySelector('.flashcard-scene');
    card.classList.remove('flipped');
    setTimeout(() => alert("Carregando próxima placa..."), 400);
}

// ==========================================
// NAVEGAÇÃO VIA HASH DA URL
// Ex.: /inicio#screen-profile → abre tela de perfil
// Usado pelos links da sidebar para abrir telas do SPA
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    var hash = window.location.hash.substring(1);
    if (hash) {
        var tela = document.getElementById(hash);
        if (tela && tela.classList.contains('screen')) {
            navigateTo(hash);
        }
    }
});
