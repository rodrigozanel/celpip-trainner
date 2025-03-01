// Função para inicializar tooltips do Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Função para atualizar a lista de questões disponíveis com base no tipo de teste selecionado
function updateQuestionsList(testTypeId) {
    if (!testTypeId) return;
    
    fetch(`/admin/questions/by_type/${testTypeId}`)
        .then(response => response.json())
        .then(data => {
            const questionsSelect = document.getElementById('questions');
            questionsSelect.innerHTML = '';
            
            data.forEach(question => {
                const option = document.createElement('option');
                option.value = question.id;
                option.textContent = question.content.substring(0, 50) + '...';
                questionsSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar questões:', error));
}

// Função para inicializar o gravador de áudio para testes de speaking
function initAudioRecorder() {
    const startButton = document.getElementById('start-recording');
    const stopButton = document.getElementById('stop-recording');
    const audioPlayer = document.getElementById('audio-player');
    const audioInput = document.getElementById('audio-file');
    
    if (!startButton || !stopButton || !audioPlayer || !audioInput) return;
    
    let mediaRecorder;
    let audioChunks = [];
    
    startButton.addEventListener('click', function() {
        audioChunks = [];
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                
                startButton.disabled = true;
                stopButton.disabled = false;
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPlayer.src = audioUrl;
                    
                    // Criar um arquivo para o input
                    const file = new File([audioBlob], 'recording.mp3', { type: 'audio/mpeg' });
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    audioInput.files = dataTransfer.files;
                });
            });
    });
    
    stopButton.addEventListener('click', function() {
        if (mediaRecorder) {
            mediaRecorder.stop();
            startButton.disabled = false;
            stopButton.disabled = true;
        }
    });
} 