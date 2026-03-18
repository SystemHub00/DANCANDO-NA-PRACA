import os
import gspread
from google.oauth2.service_account import Credentials

TEMPLATE_CONFIRMACAO = r'''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscrição realizada com sucesso!</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="/static/assistant.css">
    <link href="https://fonts.googleapis.com/css2?family=Wise:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
                .main-header {
                    border-bottom: 4px solid #de254b !important;
                }
        html, body { margin: 0; padding: 0; width: 100vw; min-height: 100vh; background: linear-gradient(120deg, #fff 60%, #de254b 100%); font-family: 'Wise', Arial, sans-serif; }
        .sucesso-container {
            max-width: 420px;
            margin: 48px auto 0 auto;
            background: #fff;
            border-radius: 28px;
            box-shadow: 0 4px 32px #de254b22, 0 1.5px 8px #de254b22;
            padding: 44px 36px 36px 36px;
            text-align: center;
            position: relative;
        }
        .checkmark {
            width: 220px;
            height: 220px;
            margin: 0 auto 18px auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .checkmark svg {
            width: 100%;
            height: 100%;
            display: block;
            stroke: #de254b;
            fill: none;
        }
        .sucesso-container h2 {
            color: #de254b;
            font-size: 1.45em;
            font-weight: 900;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }
        .sucesso-container p {
            color: #de254b;
            font-size: 1.08em;
            margin-bottom: 18px;
        }
        .protocolo-label {
            color: #de254b;
            font-size: 1.08em;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .protocolo-numero {
            color: #de254b;
            font-size: 1.35em;
            font-weight: 900;
            background: #fff0f3;
            border-radius: 10px;
            padding: 6px 0;
            margin-bottom: 8px;
            word-break: break-all;
        }
        .protocolo-box {
            margin-bottom: 18px;
        }
        .info-contato {
            color: #de254b;
            font-size: 1.05em;
            margin-bottom: 18px;
        }
        .btns {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 18px;
            width: 100%;
        }
        .btn-whatsapp, .btn-inicio {
            min-width: 180px;
            min-height: 48px;
            padding: 16px 36px;
            font-size: 1.13em;
            font-weight: 800;
            border-radius: 18px;
            border: none;
            box-shadow: 0 2px 12px #de254b33;
            letter-spacing: 0.5px;
            transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
            outline: none;
            text-transform: uppercase;
            display: inline-block;
            background: #de254b;
            color: #fff;
            cursor: pointer;
            text-decoration: none;
        }
        .btn-inicio {
            background: #fff;
            color: #de254b;
            border: 2px solid #de254b;
        }
        .btn-whatsapp:hover, .btn-inicio:hover {
            background: #de254b;
            color: #fff;
            box-shadow: 0 6px 24px #de254b44;
            transform: translateY(-2px) scale(1.04);
        }
        .proximos-passos {
            margin-top: 28px;
            color: #de254b;
            font-size: 1em;
            text-align: left;
        }
        .proximos-passos b {
            color: #de254b;
        }
        .proximos-passos ol {
            margin: 10px 0 0 18px;
            color: #de254b;
        }
        @media (max-width: 600px) {
            .sucesso-container {
                padding: 18px 6px 12px 6px;
            }
            .checkmark {
                width: 120px;
                height: 120px;
            }
            .sucesso-container h2 {
                font-size: 1.1em;
            }
            .btn-whatsapp, .btn-inicio {
                min-width: 100%;
                width: 100%;
            }
        }
    </style>
</head>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '26419185324388434');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=26419185324388434&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>
<body>
    <script src="/static/assistant.js"></script>
        <script>
        // Máscara e validação visual para o campo CEP
        document.addEventListener('DOMContentLoaded', function() {
            var cepInput = document.getElementById('cep');
            var form = document.getElementById('form-inscricao');
            if (cepInput && form) {
                let erroDivCep = document.createElement('div');
                erroDivCep.className = 'balao-erro';
                erroDivCep.id = 'cep-balao-erro';
                cepInput.parentNode.appendChild(erroDivCep);
                erroDivCep.style.display = 'none';

                function mostrarErroCep(msg) {
                    erroDivCep.textContent = msg;
                    erroDivCep.style.display = 'block';
                    cepInput.classList.add('erro-campo');
                }
                function esconderErroCep() {
                    erroDivCep.textContent = '';
                    erroDivCep.style.display = 'none';
                    cepInput.classList.remove('erro-campo');
                }
                function validarCep(cep) {
                    return /^\d{5}-\d{3}$/.test(cep);
                }
                cepInput.addEventListener('input', function() {
                    let v = cepInput.value.replace(/\D/g, '');
                    if (v.length > 8) v = v.slice(0,8);
                    let r = '';
                    if (v.length > 5) r = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
                    else r = v;
                    cepInput.value = r;
                    if (cepInput.value.length === 9 && !validarCep(cepInput.value)) {
                        mostrarErroCep('CEP inválido. Formato: 00000-000');
                    } else {
                        esconderErroCep();
                    }
                });
                form.addEventListener('submit', function(e) {
                    if (!validarCep(cepInput.value)) {
                        mostrarErroCep('CEP inválido. Formato: 00000-000');
                        cepInput.focus();
                        e.preventDefault();
                    } else {
                        esconderErroCep();
                    }
                });
            }
        });
        </script>
    <header class="main-header">
        <div class="header-logos">
            <img src="/static/logo_fgm.png" alt="Logo FGM" class="logo">
            <img src="/static/logo-prefeitura.png" alt="Prefeitura do Rio" class="logo-prefeitura-topo">
        </div>
    </header>
    <div class="sucesso-container">
        <div class="checkmark">
            <svg viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="90" stroke="#de254b" stroke-width="16" fill="none"/>
                <polyline points="60,110 95,145 145,75" stroke="#de254b" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h2>Inscrição realizada com sucesso! <span style="font-size:1.2em;">🎉</span></h2>
        <p>Você está cada vez mais perto de transformar sua vida!</p>
        <div class="protocolo-box">
            <div class="protocolo-label">Seu número de protocolo:</div>
            <div class="protocolo-numero">{{ protocolo }}</div>
            <div style="color:#7a7a7a;font-size:0.98em;margin-top:8px;">Guarde este número para acompanhar sua inscrição</div>
        </div>
        <div class="info-contato">
            <div style="margin-bottom: 18px;">
                <b>Confirmação de participação:</b><br>
                <span style="display: block; margin: 10px 0;">
                    <input type="checkbox" checked disabled style="accent-color:#de254b; margin-right:6px;"> Confirmo que resido na Ilha do Governador ou região e tenho interesse em participar do evento.
                </span>
                Confirmo que todas as informações fornecidas são verdadeiras e estou de acordo com os termos de participação.<br>
                Autorizo o uso dos meus dados para fins de inscrição e contato relacionado ao curso.<br>
                Também autorizo o uso da minha imagem para divulgação nos canais de comunicação e redes sociais do projeto e da Prefeitura do Rio de Janeiro.
            </div>
            <div style="margin-bottom: 10px;">
                <b>Ao confirmar você declara ciência de que:</b>
                <ul style="color:#de254b; margin: 8px 0 0 18px;">
                    <li>O evento é totalmente gratuito</li>
                    <li>Em caso de chuva será cancelado</li>
                    <li>Os dados serão usados apenas para inscrição</li>
                </ul>
            </div>
        </div>
        <div class="btns">
            <a class="btn-whatsapp" href="https://wa.me/?text=Acabei%20de%20me%20inscrever%20em%20um%20curso%20gratuito%20incr%C3%ADvel!%20Garanta%20sua%20vaga%20tamb%C3%A9m%20e%20venha%20transformar%20sua%20carreira%20comigo.%20Inscreva-se%20aqui:%20https://dancando-na-praca.onrender.com" target="_blank" style="display: flex; align-items: center; justify-content: center; min-width: 220px; min-height: 48px; font-size: 1.13em; font-weight: 800; border-radius: 18px; border: none; box-shadow: 0 2px 12px #de254b33; letter-spacing: 0.5px; transition: background 0.2s, box-shadow 0.2s, transform 0.1s; outline: none; text-transform: uppercase; text-align: center; margin: 0 auto 18px auto; background: #de254b; color: #fff; cursor: pointer; text-decoration: none;">&#128241; COMPARTILHAR NO WHATSAPP</a>
            <a class="btn-inicio" href="/" style="display: flex; align-items: center; justify-content: center; min-width: 220px; min-height: 48px; font-size: 1.18em; font-weight: 800; border-radius: 18px; border: 2px solid #de254b; background: #fff; color: #de254b; box-shadow: 0 2px 12px #de254b22; letter-spacing: 0.5px; transition: background 0.2s, box-shadow 0.2s, transform 0.1s; outline: none; text-transform: uppercase; text-align: center; margin: 0 auto;">VOLTAR AO INÍCIO</a>
        </div>
        <div class="proximos-passos">
            <b>Próximos Passos:</b>
            <ol>
                <li>Aguarde nosso contato via WhatsApp</li>
                <li>Prepare sua documentação (RG, CPF e comprovante de residência)</li>
                <li>Fique atenta(o) à data de início do curso</li>
                <li>Compareça no local escolhido no dia e horário marcados</li>
            </ol>
        </div>
    </div>
</body>
</html>
'''
TEMPLATE_REVISAO = r'''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Revisão</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="/static/assistant.css">
    <link href="https://fonts.googleapis.com/css2?family=Wise:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(120deg, #fff 60%, #de254b 100%);
            font-family: 'Wise', Arial, sans-serif;
        }
        .revisao-container {
            max-width: 700px;
            margin: 48px auto 0 auto;
            background: #fff;
            border-radius: 28px;
            box-shadow: 0 4px 32px rgba(0,0,0,0.10);
            padding: 44px 36px 36px 36px;
            position: relative;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #f7faff;
            border-radius: 8px;
            margin-bottom: 24px;
            overflow: hidden;
        }
        .progress {
            height: 100%;
            background: linear-gradient(90deg, #de254b 0%, #de254b 100%);
            border-radius: 8px;
            transition: width 0.3s;
            width: 100%;
        }
        .revisao-container h2 {
            font-size: 2em;
            font-weight: 900;
            color: #de254b;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }
        .revisao-sub {
            color: #de254b;
            font-size: 1.08em;
            margin-bottom: 24px;
        }
        .info-box {
            background: #fff0f3;
            border-radius: 16px;
            border: 2px solid #de254b;
            margin-bottom: 18px;
            padding: 18px 22px;
        }
        .info-title {
            font-weight: 700;
            color: #de254b;
            margin-bottom: 8px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .info-title svg {
            width: 20px;
            height: 20px;
        }
        .info-content {
            color: #de254b;
            font-size: 1.08em;
        }
        .confirmacao-box {
            background: #fff0f3;
            border-radius: 16px;
            border: 2px solid #de254b;
            margin-bottom: 18px;
            padding: 18px 22px;
        }
        .confirmacao-box label {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 1.05em;
            color: #de254b;
            cursor: pointer;
        }
        .form-btns {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: stretch;
            margin-top: 18px;
            gap: 12px;
        }
        .btn-voltar, .btn-finalizar {
            min-width: 200px;
            background: linear-gradient(90deg, #de254b 0%, #de254b 100%);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 18px 40px;
            font-size: 1.18em;
            font-weight: 800;
            font-family: 'Wise', Arial, sans-serif;
            cursor: pointer;
            box-shadow: 0 2px 8px #de254b22;
            letter-spacing: 0.5px;
            transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
            outline: none;
            text-transform: uppercase;
            display: inline-block;
        }
        .btn-finalizar:disabled {
            background: #de254b;
            color: #fff;
            cursor: not-allowed;
        }
        .btn-finalizar:hover:enabled {
            background: linear-gradient(90deg, #de254b 0%, #de254b 100%);
            box-shadow: 0 4px 16px #de254b44;
        }
        .btn-voltar:hover {
            background: #fff0f3;
            color: #de254b;
        }
        @media (max-width: 600px) {
            .revisao-container {
                padding: 18px 6px 12px 6px;
            }
            .revisao-container h2 {
                font-size: 1.3em;
            }
        }
    </style>
</head>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '26419185324388434');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=26419185324388434&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>
<body>
    <script src="/static/assistant.js"></script>
    <header class="main-header">
        <div class="header-logos">
            <img src="/static/logo_fgm.png" alt="Logo FGM" class="logo">
            <img src="/static/logo-prefeitura.png" alt="Prefeitura do Rio" class="logo-prefeitura-topo">
        </div>
    </header>
    <div class="revisao-container">
        <form method="POST" action="/revisao" autocomplete="off">
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
            <div style="color:#de254b;font-weight:600;margin-bottom:18px;">&#127881; Formulário completo! Revise seus dados antes de finalizar.</div>
            <h2 style="color:#de254b;">Revise suas Informações</h2>
            <p class="revisao-sub" style="color:#de254b;">Confira se está tudo certo antes de finalizar</p>
            <!-- Blocos dinâmicos de informações preenchidas -->
            <div class="info-box">
                <div class="info-title">&#128100; Dados Pessoais</div>
                <div class="info-content">
                    Nome: {{ dados.get('nome', '') }}<br>
                    CPF: {{ dados.get('cpf', '') }}<br>
                    Data de Nascimento: {{ dados.get('nascimento', '') }}<br>
                    Gênero: {{ dados.get('genero', '') }}<br>
                    Email: {{ dados.get('email', '') }}<br>
                    WhatsApp: {{ dados.get('whatsapp', '') }}
                </div>
            </div>
            <div class="info-box">
                <div class="info-title">&#127891; Curso Escolhido</div>
                <div class="info-content">
                    Curso: {{ dados.get('curso', '') }}<br>
                    Local: {{ dados.get('local', '') }}<br>
                    Turma: {{ dados.get('turma', '') }}<br>
                    Horário: {{ dados.get('horario', '') }}<br>
                    Data de Início: {{ dados.get('data_inicio', '') }}<br>
                    Encerramento: {{ dados.get('encerramento', '') }}<br>
                    Endereço: {{ dados.get('endereco_curso', '') }}
                </div>
            </div>
            <div class="form-group" style="background: #fff0f3; border: 2px solid #de254b; border-radius: 16px; padding: 18px 22px; margin-bottom: 18px; box-shadow: 0 2px 12px #de254b22;">
                <label for="como_conheceu" style="font-weight:700; color:#de254b; margin-bottom:7px; font-size:1.09em; display:block; width:100%; max-width:380px;">Como conheceu:</label>
                <input type="text" id="como_conheceu" name="como_conheceu" placeholder="Digite como conheceu o projeto" value="{{ dados.get('como_conheceu', '') }}" style="border:1.5px solid #de254b; color:#222; background:#fff0f3; box-shadow:0 2px 12px #de254b22; transition:border 0.2s, box-shadow 0.2s; border-radius:14px; padding:13px 18px; font-size:1.09em; font-family:'Wise', Arial, sans-serif; outline:none; width:100%; max-width:380px; min-width:220px; margin:0 auto; display:block;">
            </div>
            <div class="confirmacao-box">
                <label><input type="checkbox" id="confirma-dados">&nbsp;Confirmo que todas as informações fornecidas são verdadeiras e estou de acordo com os termos de participação. Autorizo o uso dos meus dados para fins de inscrição e contato relacionado ao curso.<br><br>
                Também autorizo o uso da minha imagem para divulgação nos canais de comunicação e redes sociais do projeto e da Prefeitura do Rio de Janeiro.<br><br>
                Estou ciente de que o certificado de conclusão só será emitido para alunos considerados aptos, após avaliação do professor responsável pelo curso.</label>
            </div>
            <div class="form-btns" style="display:flex; flex-direction:column !important; gap:12px; width:100%; margin-top:18px;">
                <button type="submit" class="btn-finalizar" id="btn-finalizar" disabled style="margin-bottom:0;">Finalizar Inscrição</button>
                <button type="button" class="btn-voltar">&lt; Voltar</button>
            </div>
        </form>
    </div>
    <script>
        document.querySelector('.btn-voltar').onclick = function() {
            window.location.href = '/curso';
        };
        document.getElementById('confirma-dados').addEventListener('change', function() {
            document.getElementById('btn-finalizar').disabled = !this.checked;
        });
    </script>
</body>
</html>
'''
TEMPLATE_CURSO = r'''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Escolha do Curso</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="/static/assistant.css">
    <link href="https://fonts.googleapis.com/css2?family=Wise:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        html, body { min-height: 100vh; height: 100%; margin: 0; padding: 0; }
        body { min-height: 100vh; min-height: 100svh; height: 100%; width: 100vw; background: linear-gradient(120deg, #fff 60%, #de254b 100%); font-family: 'Wise', 'Segoe UI', Arial, sans-serif; background-repeat: no-repeat; background-attachment: fixed; }
        .curso-container { max-width: 480px; margin: 48px auto 0 auto; background: #fff; border-radius: 32px; box-shadow: 0 8px 40px #de254b22, 0 1.5px 8px #de254b22; padding: 48px 36px 36px 36px; text-align: center; position: relative; }
        .progress-bar { width: 100%; height: 8px; background: #fff0f3; border-radius: 8px; margin-bottom: 24px; overflow: hidden; }
        .progress { height: 100%; background: linear-gradient(90deg, #de254b 0%, #de254b 100%); border-radius: 8px; transition: width 0.3s; width: 99%; }
        .curso-container h2 { font-size: 2em; font-weight: 900; color: #de254b; margin-bottom: 8px; letter-spacing: -1px; }
        .curso-sub { color: #de254b; font-size: 1.08em; margin-bottom: 24px; }
        .form-group { margin-bottom: 18px; text-align: left; width: 100%; display: flex; flex-direction: column; align-items: center; }
        .form-group label { font-weight: 600; color: #de254b; margin-bottom: 7px; font-size: 1.09em; display: block; width: 100%; max-width: 380px; }
        .form-group input[type="text"] { border: 1.5px solid #de254b; color: #111 !important; background: #fff0f3; box-shadow: 0 2px 12px #de254b22; transition: border 0.2s, box-shadow 0.2s; border-radius: 14px; padding: 13px 18px; font-size: 1.09em; font-family: 'Wise', Arial, sans-serif; outline: none; appearance: none; width: 100%; max-width: 380px; min-width: 220px; margin: 0 auto; display: block; }
        .form-group input[type="text"]:focus { border: 2px solid #de254b; box-shadow: 0 4px 16px #de254b33; background: #fff; }
        .form-group input[type="text"]::placeholder { color: #de254b; opacity: 1; }
        .curso-container input, .curso-container select { border: 1.5px solid #de254b; color: #111 !important; background: #fff0f3; box-shadow: 0 2px 12px #de254b22; transition: border 0.2s, box-shadow 0.2s; border-radius: 14px; padding: 13px 18px; font-size: 1.09em; font-family: 'Wise', Arial, sans-serif; outline: none; appearance: none; width: 100%; max-width: 380px; min-width: 220px; margin: 0 auto; display: block; }
        .curso-container input:focus, .curso-container select:focus { border: 2px solid #de254b; box-shadow: 0 4px 16px #de254b33; background: #fff; }
        .curso-container input::placeholder { color: #de254b; opacity: 1; }
        .curso-container select { appearance: none; -webkit-appearance: none; -moz-appearance: none; background-image: url('data:image/svg+xml;utf8,<svg fill="%23de254b" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>'); background-repeat: no-repeat; background-position: right 14px center; background-size: 22px 22px; }
        .form-btns { display: flex; flex-direction: column; justify-content: flex-start; align-items: stretch; margin-top: 24px; gap: 12px; width: 100%; }
        .btn-voltar, .btn-proximo { min-width: 180px; min-height: 48px; padding: 16px 36px; font-size: 1.18em; font-weight: 800; border-radius: 18px; border: none; box-shadow: 0 2px 12px #de254b33; letter-spacing: 0.5px; transition: background 0.2s, box-shadow 0.2s, transform 0.1s; outline: none; text-transform: uppercase; display: inline-block; background: #de254b; color: #fff; cursor: pointer; }
        .btn-voltar { background: #fff; color: #de254b; border: 2px solid #de254b; }
        .btn-proximo { background: #de254b; color: #fff; border: 2px solid #de254b; }
        .btn-proximo:hover, .btn-voltar:hover { background: #de254b; color: #fff; box-shadow: 0 6px 24px #de254b44; transform: translateY(-2px) scale(1.04); }
        @media (max-width: 600px) { .curso-container { padding: 18px 6px 12px 6px; } .curso-container h2 { font-size: 1.3em; } .form-btns { flex-direction: column; gap: 16px; width: 100%; } .btn-voltar, .btn-proximo { min-width: 100%; width: 100%; } }
        @media (max-width: 600px) { .curso-container { padding: 18px 6px 12px 6px; } .curso-container h2 { font-size: 1.3em; } .form-btns { flex-direction: column; gap: 12px; width: 100%; } }
    </style>
</head>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '26419185324388434');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=26419185324388434&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>
<body>
    <script src="/static/assistant.js"></script>
    <header class="main-header">
        <div class="header-logos">
            <img src="/static/logo_fgm.png" alt="Logo FGM" class="logo">
            <img src="/static/logo-prefeitura.png" alt="Prefeitura do Rio" class="logo-prefeitura-topo">
        </div>
    </header>
    <div class="curso-container">
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
        <h2>Escolha do Curso</h2>
        <p class="curso-sub">Selecione o local, curso e turma de sua preferência</p>
        <form id="form-curso" method="POST" action="/curso" autocomplete="off">
            <div class="form-group">
                <label for="local">Local *</label>
                <select id="local" name="local" required>
                    <option value="ILHA DO GOVERNADOR">ILHA DO GOVERNADOR</option>
                </select>
            </div>
            <div class="form-group">
                <label for="curso">Ritmo *</label>
                <select id="curso" name="curso" required>
                    <option value="FORRÓ, GAFIEIRA E SAMBA NO PÉ">FORRÓ, GAFIEIRA E SAMBA NO PÉ</option>
                </select>
            </div>
            <div class="form-group">
                <label for="turma">Evento *</label>
                <select id="turma" name="turma" required>
                    <option value="ANFITEATRO ATERRO DO COCOTÁ">ANFITEATRO ATERRO DO COCOTÁ</option>
                </select>
            </div>
            <div class="form-group">
                <label for="horario">Dia/Horário</label>
                <input type="text" id="horario" name="horario" value="Domingo | 17h" readonly />
            </div>
            <div class="form-group">
                <label for="data_inicio">Data de Início</label>
                <input type="text" id="data_inicio" name="data_inicio" value="22/03/2026" readonly />
            </div>
            <div class="form-group">
                <label for="encerramento">Aviso</label>
                <input type="text" id="encerramento" name="encerramento" value="⚠️Em caso de chuva pode ser cancelado" readonly />
            </div>
            <div class="form-group">
                <label for="endereco">Endereço</label>
                <input type="text" id="endereco" name="endereco" value="📍Parque Poeta Manuel Bandeira, s/n, Aterro do Cocotá, Ilha do Governador, RJ. (ANFITEATRO)" readonly />
            </div>
            <div class="form-btns" style="display:flex; flex-direction:column !important; gap:12px; width:100%; margin-top:24px;">
                <button type="submit" class="btn-proximo">PRÓXIMO &rarr;</button>
                <button type="button" class="btn-voltar" onclick="window.location.href='/endereco'">&lt; VOLTAR</button>
            </div>
        </form>
    </div>
    <script>
    // Não é necessário JS dinâmico pois só há uma opção fixa para cada campo
    const enderecoInput = document.getElementById('endereco');

    function resetCursos() {
        cursoSelect.innerHTML = '<option value="">Selecione o curso</option>';
        resetCampos();
    }

    function resetCampos() {
        turmaSelect.innerHTML = '<option value="">Selecione a turma</option>';
        horarioInput.value = '';
        dataInicioInput.value = '';
        encerramentoInput.value = '';
        enderecoInput.value = '';
    }

    localSelect.addEventListener('change', function() {
        resetCursos();
        const local = this.value;
        if (cursosPorLocal[local]) {
            cursosPorLocal[local].forEach(function(curso) {
                const opt = document.createElement('option');
                opt.value = curso;
                opt.textContent = curso;
                cursoSelect.appendChild(opt);
            });
        }
    });

    cursoSelect.addEventListener('change', function() {
        resetCampos();
        const local = localSelect.value;
        const curso = this.value;
        if (turmasData[local] && turmasData[local][curso]) {
            turmasData[local][curso].forEach(function(turmaObj) {
                const opt = document.createElement('option');
                opt.value = turmaObj.turma;
                opt.textContent = turmaObj.turma;
                turmaSelect.appendChild(opt);
            });
        }
    });

    turmaSelect.addEventListener('change', function() {
        const local = localSelect.value;
        const curso = cursoSelect.value;
        const turma = this.value;
        if (turmasData[local] && turmasData[local][curso]) {
            const turmaObj = turmasData[local][curso].find(t => t.turma === turma);
            if (turmaObj) {
                horarioInput.value = turmaObj.horario;
                dataInicioInput.value = turmaObj.data_inicio;
                encerramentoInput.value = turmaObj.encerramento;
                enderecoInput.value = turmaObj.endereco;
            } else {
                horarioInput.value = '';
                dataInicioInput.value = '';
                encerramentoInput.value = '';
                enderecoInput.value = '';
            }
        }
    });
    </script>
</body>
</html>
'''
TEMPLATE_INSCRICAO = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inscrição</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="/static/assistant.css">
    <link href="https://fonts.googleapis.com/css2?family=Wise:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        html, body {
            height: 100%;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }
        html, body {
            min-height: 100vh;
            height: 100%;
            margin: 0;
            padding: 0;
        }
        body {
            min-height: 100vh;
            min-height: 100svh;
            height: 100%;
            width: 100vw;
            background: linear-gradient(120deg, #fff 60%, #de254b 100%);
            font-family: 'Wise', 'Segoe UI', Arial, sans-serif;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .inscricao-container {
            max-width: 480px;
            margin: 48px auto 0 auto;
            background: #fff;
            border-radius: 32px;
            box-shadow: 0 8px 40px rgba(222,37,75,0.13), 0 1.5px 8px #de254b22;
            border-top: 4px solid #de254b;
            padding: 48px 36px 36px 36px;
            text-align: center;
            position: relative;
        }
        .inscricao-numero {
            color: #de254b;
            font-weight: 700;
            margin-bottom: 10px;
            font-size: 1.08em;
        }
        .inscricao-container {
            max-width: 480px;
            margin: 48px auto 0 auto;
            background: #fff;
            border-radius: 32px;
            box-shadow: 0 8px 40px rgba(222,37,75,0.13), 0 1.5px 8px #de254b22;
            padding: 48px 36px 36px 36px;
            text-align: center;
            position: relative;
        }
        .main-header {
            border-bottom: 4px solid #de254b;
        }
            margin-bottom: 28px;
        }
        .inscricao-container form {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
        }
        .form-group {
            margin-bottom: 18px;
            text-align: left;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .form-group label {
            font-weight: 600;
            color: #de254b !important;
            margin-bottom: 7px;
            font-size: 1.09em;
            display: block;
            width: 100%;
            max-width: 340px;
        }
        .inscricao-container input, .inscricao-container select {
            border: 1.5px solid #de254b !important;
            color: #de254b !important;
            background: #f7faff;
            box-shadow: 0 2px 12px #de254b22;
            transition: border 0.2s, box-shadow 0.2s;
            border-radius: 14px;
            padding: 13px 18px;
            font-size: 1.09em;
            font-family: 'Wise', Arial, sans-serif;
            outline: none;
            appearance: none;
            width: 100%;
            max-width: 380px;
            margin: 0 auto;
            display: block;
        }
        .inscricao-container input:focus, .inscricao-container select:focus {
            border: 2px solid #de254b;
            box-shadow: 0 4px 16px #de254b33;
            background: #fff;
        }
        .inscricao-container input::placeholder {
            color: #b3a0d7;
            opacity: 1;
        }
        .inscricao-container select {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            background-image: url('data:image/svg+xml;utf8,<svg fill="%23de254b" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
            background-repeat: no-repeat;
            background-position: right 14px center;
            background-size: 22px 22px;
            width: 100% !important;
            max-width: 380px !important;
        }
        .balao-erro {
            display: block;
            position: relative;
            background: #e53935;
            color: #fff;
            border: 2px solid #b71c1c;
            border-radius: 16px 16px 16px 0px;
            padding: 10px 16px;
            font-size: 1em;
            font-weight: 600;
            box-shadow: 0 4px 16px #b71c1c33;
            margin-top: 8px;
            max-width: 340px;
            text-align: left;
        }
        .balao-erro::after {
            content: '';
            position: absolute;
            left: 24px;
            bottom: 100%;
            width: 0;
            height: 0;
            border-bottom: 12px solid #e53935;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
        }
        .form-group label {
            font-weight: 600;
            color: #1155cc;
            margin-bottom: 7px;
            font-size: 1.09em;
            display: block;
            width: 100%;
            max-width: 400px;
        }
        .inscricao-container input, .inscricao-container select {
            color: #111 !important;
            border: 1.5px solid #b3a0d7;
            color: #222;
            background: #f7faff;
            box-shadow: 0 2px 12px #b3a0d722;
            transition: border 0.2s, box-shadow 0.2s;
            border-radius: 14px;
            padding: 13px 18px;
            font-size: 1.09em;
            font-family: 'Wise', Arial, sans-serif;
            outline: none;
            appearance: none;
            width: 100%;
            max-width: 400px;
            min-width: 220px;
            margin: 0 auto;
            display: block;
        }
        .inscricao-container select {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            background-image: url('data:image/svg+xml;utf8,<svg fill="%231155cc" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/></svg>');
            background-repeat: no-repeat;
            background-position: right 14px center;
            background-size: 22px 22px;
        }
            }
            .form-btns {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                margin-top: 24px;
                gap: 18px;
                width: 100%;
            }
            .btn-voltar, .btn-proximo {
                min-width: 180px;
                min-height: 48px;
                padding: 16px 36px;
                font-size: 1.18em;
                font-weight: 800;
                border-radius: 18px;
                border: none;
                box-shadow: 0 2px 12px #de254b33;
                letter-spacing: 0.5px;
                transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
                outline: none;
                text-transform: uppercase;
                display: inline-block;
                background: #de254b;
                color: #fff;
                cursor: pointer;
            }
            .btn-voltar {
                background: #fff;
                color: #de254b;
                border: 2px solid #de254b;
            }
            .btn-proximo {
                background: #de254b;
                color: #fff;
                border: 2px solid #de254b;
            }
            .btn-proximo:hover, .btn-voltar:hover {
                background: #de254b;
                color: #fff;
                box-shadow: 0 6px 24px #de254b44;
                transform: translateY(-2px) scale(1.04);
            }
            @media (max-width: 600px) {
                .inscricao-container {
                    padding: 18px 6px 12px 6px;
                }
                .inscricao-container h2 {
                    font-size: 1.3em;
                }
                .form-btns {
                    flex-direction: column;
                    gap: 16px;
                    width: 100%;
                }
                .btn-voltar, .btn-proximo {
                    min-width: 100%;
                    width: 100%;
                }
            }
        }
    </style>
</head>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '26419185324388434');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=26419185324388434&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>
<body>
    <script src="/static/assistant.js"></script>
    <script>
    // Validação visual do WhatsApp (DDD 55) com balão de erro
    document.addEventListener('DOMContentLoaded', function() {
        var whatsappInput = document.getElementById('whatsapp');
        var form = document.getElementById('form-inscricao');
        if (whatsappInput && form) {
            let erroDivWpp = document.getElementById('whatsapp-balao-erro');
            if (!erroDivWpp) {
                erroDivWpp = document.createElement('div');
                erroDivWpp.className = 'balao-erro';
                erroDivWpp.id = 'whatsapp-balao-erro';
                whatsappInput.parentNode.appendChild(erroDivWpp);
            }
            erroDivWpp.style.display = 'none';

            function mostrarErroWpp(msg) {
                erroDivWpp.textContent = msg;
                erroDivWpp.style.display = 'block';
                whatsappInput.classList.add('erro-campo');
            }
            function esconderErroWpp() {
                erroDivWpp.textContent = '';
                erroDivWpp.style.display = 'none';
                whatsappInput.classList.remove('erro-campo');
            }
            function ddd55Invalido(val) {
                return /^\(55\)/.test(val);
            }
            whatsappInput.addEventListener('input', function() {
                if (ddd55Invalido(whatsappInput.value)) {
                    mostrarErroWpp('Não utilize o DDD 55. Informe o DDD local, ex: (21)');
                } else {
                    esconderErroWpp();
                }
            });
            form.addEventListener('submit', function(e) {
                if (ddd55Invalido(whatsappInput.value)) {
                    mostrarErroWpp('Não utilize o DDD 55. Informe o DDD local, ex: (21)');
                    whatsappInput.focus();
                    e.preventDefault();
                } else {
                    esconderErroWpp();
                }
            });
        }
    });
    </script>
    <script>
    // Validação visual de CPF, Email e Idade mínima
    document.addEventListener('DOMContentLoaded', function() {
        var cpfInput = document.getElementById('cpf');
        var emailInput = document.getElementById('email');
        var nascInput = document.getElementById('nascimento');
        var form = document.getElementById('form-inscricao');
        // CPF
        if (cpfInput && form) {
            let erroDiv = document.getElementById('cpf-balao-erro');
            if (!erroDiv) {
                erroDiv = document.createElement('div');
                erroDiv.className = 'balao-erro';
                erroDiv.id = 'cpf-balao-erro';
                cpfInput.parentNode.appendChild(erroDiv);
            }
            erroDiv.style.display = 'none';

            function validarCPF(cpf) {
                cpf = cpf.replace(/\D/g, '');
                if (cpf.length !== 11 || /^([0-9])\1+$/.test(cpf)) return false;
                let soma = 0;
                for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
                let digito1 = (soma * 10) % 11;
                if (digito1 === 10) digito1 = 0;
                if (digito1 !== parseInt(cpf.charAt(9))) return false;
                soma = 0;
                for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
                let digito2 = (soma * 10) % 11;
                if (digito2 === 10) digito2 = 0;
                if (digito2 !== parseInt(cpf.charAt(10))) return false;
                return true;
            }

            function mostrarErroCPF(msg) {
                erroDiv.textContent = msg;
                erroDiv.style.display = 'block';
                cpfInput.classList.add('erro-campo');
            }
            function esconderErroCPF() {
                erroDiv.textContent = '';
                erroDiv.style.display = 'none';
                cpfInput.classList.remove('erro-campo');
            }

            cpfInput.addEventListener('input', function() {
                if (cpfInput.value.replace(/\D/g, '').length === 11) {
                    if (!validarCPF(cpfInput.value)) {
                        mostrarErroCPF('CPF inválido. Verifique e digite novamente.');
                    } else {
                        esconderErroCPF();
                    }
                } else {
                    esconderErroCPF();
                }
            });

            form.addEventListener('submit', function(e) {
                if (!validarCPF(cpfInput.value)) {
                    mostrarErroCPF('CPF inválido. Verifique e digite novamente.');
                    cpfInput.focus();
                    e.preventDefault();
                } else {
                    esconderErroCPF();
                }
            });
        }
        // EMAIL
        if (emailInput && form) {
            let erroDivEmail = document.getElementById('email-balao-erro');
            if (!erroDivEmail) {
                erroDivEmail = document.createElement('div');
                erroDivEmail.className = 'balao-erro';
                erroDivEmail.id = 'email-balao-erro';
                emailInput.parentNode.appendChild(erroDivEmail);
            }
            erroDivEmail.style.display = 'none';

            function validarEmail(email) {
                // Aceita apenas gmail, hotmail, outlook, yahoo
                var re = /^[a-zA-Z0-9_.+-]+@((gmail|hotmail|outlook|yahoo)\.(com|com\.br))$/i;
                return re.test(email.trim());
            }
            function mostrarErroEmail(msg) {
                erroDivEmail.textContent = msg;
                erroDivEmail.style.display = 'block';
                emailInput.classList.add('erro-campo');
            }
            function esconderErroEmail() {
                erroDivEmail.textContent = '';
                erroDivEmail.style.display = 'none';
                emailInput.classList.remove('erro-campo');
            }
            emailInput.addEventListener('input', function() {
                if (emailInput.value.length > 0) {
                    if (!validarEmail(emailInput.value)) {
                        mostrarErroEmail('Digite um e-mail válido do Gmail, Hotmail, Outlook ou Yahoo.');
                    } else {
                        esconderErroEmail();
                    }
                } else {
                    esconderErroEmail();
                }
            });
            form.addEventListener('submit', function(e) {
                if (!validarEmail(emailInput.value)) {
                    mostrarErroEmail('Digite um e-mail válido do Gmail, Hotmail, Outlook ou Yahoo.');
                    emailInput.focus();
                    e.preventDefault();
                } else {
                    esconderErroEmail();
                }
            });
        }
        // IDADE MÍNIMA 16 ANOS
        if (nascInput && form) {
            let erroDivNasc = document.getElementById('nascimento-balao-erro');
            if (!erroDivNasc) {
                erroDivNasc = document.createElement('div');
                erroDivNasc.className = 'balao-erro';
                erroDivNasc.id = 'nascimento-balao-erro';
                nascInput.parentNode.appendChild(erroDivNasc);
            }
            erroDivNasc.style.display = 'none';

            function idadeMinima16(nascStr) {
                // Aceita dd/mm/aaaa
                var partes = nascStr.split('/');
                if (partes.length !== 3) return false;
                var dia = parseInt(partes[0], 10);
                var mes = parseInt(partes[1], 10) - 1;
                var ano = parseInt(partes[2], 10);
                var nascDate = new Date(ano, mes, dia);
                if (isNaN(nascDate.getTime())) return false;
                var hoje = new Date();
                var idade = hoje.getFullYear() - nascDate.getFullYear();
                var m = hoje.getMonth() - nascDate.getMonth();
                if (m < 0 || (m === 0 && hoje.getDate() < nascDate.getDate())) {
                    idade--;
                }
                return idade >= 16 && idade <= 90;
            }
            function mostrarErroNasc(msg) {
                erroDivNasc.textContent = msg;
                erroDivNasc.style.display = 'block';
                nascInput.classList.add('erro-campo');
            }
            function esconderErroNasc() {
                erroDivNasc.textContent = '';
                erroDivNasc.style.display = 'none';
                nascInput.classList.remove('erro-campo');
            }
            nascInput.addEventListener('blur', function() {
                if (nascInput.value.length === 10) {
                    if (!idadeMinima16(nascInput.value)) {
                        mostrarErroNasc('Idade permitida: de 16 até 90 anos');
                    } else {
                        esconderErroNasc();
                    }
                } else {
                    esconderErroNasc();
                }
            });
            form.addEventListener('submit', function(e) {
                if (!idadeMinima16(nascInput.value)) {
                    mostrarErroNasc('Idade permitida: de 16 até 90 anos');
                    nascInput.focus();
                    e.preventDefault();
                } else {
                    esconderErroNasc();
                }
            });
        }
    });
    </script>
    <script>
    // Máscara para CPF
    document.addEventListener('DOMContentLoaded', function() {
        var cpf = document.getElementById('cpf');
        if (cpf) {
            cpf.addEventListener('input', function(e) {
                let v = cpf.value.replace(/\D/g, '');
                if (v.length > 11) v = v.slice(0,11);
                let r = '';
                if (v.length > 9) r = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
                else if (v.length > 6) r = v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
                else if (v.length > 3) r = v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
                else r = v;
                cpf.value = r;
            });
        }
        // Máscara para Data de Nascimento
        var nasc = document.getElementById('nascimento');
        if (nasc) {
            nasc.addEventListener('input', function(e) {
                let v = nasc.value.replace(/\D/g, '');
                if (v.length > 8) v = v.slice(0,8);
                let r = '';
                if (v.length > 4) r = v.replace(/(\d{2})(\d{2})(\d{1,4})/, '$1/$2/$3');
                else if (v.length > 2) r = v.replace(/(\d{2})(\d{1,2})/, '$1/$2');
                else r = v;
                nasc.value = r;
            });
        }
        // Máscara para WhatsApp
        var wpp = document.getElementById('whatsapp');
        if (wpp) {
            wpp.addEventListener('input', function(e) {
                let v = wpp.value.replace(/\D/g, '');
                if (v.length > 11) v = v.slice(0,11);
                let r = '';
                if (v.length > 6) r = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
                else if (v.length > 2) r = v.replace(/(\d{2})(\d{1,5})/, '($1) $2');
                else r = v;
                wpp.value = r;
            });
        }
    });
    </script>
    <header class="main-header">
        <div class="header-logos">
            <img src="/static/logo_fgm.png" alt="Logo FGM" class="logo">
            <img src="/static/logo-prefeitura.png" alt="Prefeitura do Rio" class="logo-prefeitura-topo">
        </div>
    </header>
    <div class="inscricao-container">
        <div class="progress-bar">
            <div class="progress" style="width: 33%;"></div>
        </div>
        <h2 style="color: #de254b !important; text-shadow: none !important; background: none !important;">Dados Pessoais</h2>
        <p class="inscricao-sub">Preencha seus dados para começarmos sua inscrição</p>
        <form id="form-inscricao" method="POST" action="/inscricao" autocomplete="off">
            <div class="form-group">
                <label for="nome">Nome Completo *</label>
                <input type="text" id="nome" name="nome" placeholder="Digite seu nome completo" required maxlength="50" pattern="[A-Za-zÀ-ÿ '´`^~.-]+">
                {% if erro_nome %}
                <div class="balao-erro" id="nome-balao-erro">{{ erro_nome }}</div>
                {% endif %}
            </div>
            <div class="form-group">
                <label for="genero">Gênero *</label>
                <select id="genero" name="genero" required>
                    <option value="">Selecione</option>
                    <option value="Feminino">Feminino</option>
                    <option value="Masculino">Masculino</option>
                    <option value="Outro">Outro</option>
                    <option value="Prefiro não dizer">Prefiro não dizer</option>
                </select>
                {% if erro_genero %}
                <div class="balao-erro" id="genero-balao-erro">{{ erro_genero }}</div>
                {% endif %}
            </div>
            <div class="form-group">
                <label for="cpf">CPF *</label>
                <input type="text" id="cpf" name="cpf" placeholder="000.000.000-00" required maxlength="14" pattern="\d{3}\.\d{3}\.\d{3}-\d{2}" title="Digite um CPF válido">
                {% if erro_cpf %}
                <div class="balao-erro" id="cpf-balao-erro">{{ erro_cpf }}</div>
                {% endif %}
            </div>
            <div class="form-group">
                <label for="nascimento">Data de Nascimento *</label>
                <input type="text" id="nascimento" name="nascimento" placeholder="dd/mm/aaaa" required maxlength="10" pattern="\d{2}/\d{2}/\d{4}">
                {% if erro_nascimento %}
                <div class="balao-erro" id="nascimento-balao-erro">{{ erro_nascimento }}</div>
                {% endif %}
            </div>
            <div class="form-group">
                <label for="whatsapp">WhatsApp *</label>
                <input type="text" id="whatsapp" name="whatsapp" placeholder="(00) 00000-0000" required maxlength="16" pattern="\(\d{2}\) \d{5}-\d{4}">
                {% if erro_whatsapp %}
                <div class="balao-erro" id="whatsapp-balao-erro">{{ erro_whatsapp }}</div>
                {% endif %}
            </div>
            <div class="form-group">
                <label for="cep">CEP *</label>
                <input type="text" id="cep" name="cep" placeholder="00000-000" required maxlength="9" pattern="\d{5}-\d{3}">
                            <script>
                            // Máscara automática para CEP (00000-000)
                            document.addEventListener('DOMContentLoaded', function() {
                                var cepInput = document.getElementById('cep');
                                if (cepInput) {
                                    cepInput.addEventListener('input', function(e) {
                                        let v = cepInput.value.replace(/\D/g, '');
                                        if (v.length > 8) v = v.slice(0,8);
                                        let r = '';
                                        if (v.length > 5) r = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
                                        else r = v;
                                        cepInput.value = r;
                                    });
                                }
                            });
                            </script>
            </div>
            <div class="form-group">
                <label for="bairro">Bairro *</label>
                <input type="text" id="bairro" name="bairro" placeholder="Nome do bairro" required maxlength="40">
            </div>
            <div class="form-group">
                <label for="email">E-mail *</label>
                <input type="email" id="email" name="email" placeholder="seuemail@exemplo.com" required maxlength="60" pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" title="Digite um e-mail válido">
                {% if erro_email %}
                <div class="balao-erro" id="email-balao-erro">{{ erro_email }}</div>
                {% endif %}
            </div>
            <div class="form-btns" style="display:flex; flex-direction:column !important; gap:12px; width:100%; margin-top:24px;">
                <button type="submit" class="btn-proximo">PRÓXIMO &rarr;</button>
                <button type="button" class="btn-voltar" onclick="window.location.href='/'">&lt; VOLTAR</button>
            </div>
        </form>
    </div>
</body>
</html>
'''
from flask import Flask, render_template_string, request, redirect, url_for, session
import csv
import uuid
import os

from gsheet_utils import append_to_sheet
import traceback


TEMPLATE_INDEX = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FGM</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="stylesheet" href="/static/assistant.css">
    <link href="https://fonts.googleapis.com/css2?family=Wise:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(120deg, #fff 60%, #de254b 100%);
            font-family: 'Wise', Arial, sans-serif;
        }
        .benefits {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-gap: 24px;
            max-width: 800px;
            margin: 18px auto 0 auto;
        }
        .benefit {
            min-width: 220px;
            max-width: 520px;
            width: 50%;
            min-height: 44px;
            height: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            background: linear-gradient(90deg, #fff 80%, #eaf2fb 100%);
            border: 1.5px solid #b3d1ff;
            border-radius: 18px;
            box-shadow: 0 2px 12px #de254b22, 0 1.5px 8px #de254b11;
            font-size: 1.08em;
            color: #de254b;
            font-weight: 700;
            margin: 10px auto;
            padding: 10px 18px;
            transition: box-shadow 0.25s, transform 0.18s, background 0.18s;
            cursor: pointer;
            white-space: normal;
            overflow-wrap: break-word;
            word-break: break-word;
            text-align: center;
        }
        .benefit:hover {
            box-shadow: 0 6px 24px #de254b44, 0 2px 12px #de254b22;
            background: linear-gradient(90deg, #eaf2fb 60%, #fff 100%);
            transform: translateY(-2px) scale(1.03);
        }
        @media (max-width: 700px) {
            .benefits {
                grid-template-columns: 1fr;
            }
        }
        h1, h2, h3, h4, h5, h6 {
            color: #de254b;
            font-family: 'Wise', Arial, sans-serif;
        }
        .cta-btn {
            display: inline-block;
            background: linear-gradient(90deg, #de254b 0%, #de254b 100%);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 16px 40px;
            font-size: 1.18em;
            font-weight: 800;
            font-family: 'Wise', Arial, sans-serif;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(222,37,75,0.10);
            letter-spacing: 0.5px;
            transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
            outline: none;
            text-transform: uppercase;
            margin-top: 18px;
            text-decoration: none;
        }
        .cta-btn:hover {
            background: linear-gradient(90deg, #de254b 0%, #de254b 100%);
            box-shadow: 0 4px 16px rgba(222,37,75,0.12);
        }
        .ganhos-box, .cursos-section, .contato-section {
            background: #fff;
            border-radius: 16px;
            border: 2px solid #de254b;
            margin: 24px 0;
            padding: 18px 22px;
        }
        .ganhos-list li, .cursos-title, .cursos-destaque, .contato-section p, .contato-section h2 {
            color: #de254b;
        }
        .icon-svg svg {
            stroke: #de254b !important;
        }
        .main-header, footer {
            background: #fff;
        }
        .main-header {
            border-bottom: 4px solid #de254b;
        }
        footer {
            border-top: 4px solid #de254b;
        }
        footer p {
            color: #de254b;
        }
    </style>
</head>
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '26419185324388434');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=26419185324388434&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</head>
<body>
    <script src="/static/assistant.js"></script>
    <script>
    // Validação de CPF válido
    function validarCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        if (cpf.length !== 11 || /^([0-9])\1+$/.test(cpf)) return false;
        let soma = 0, resto;
        for (let i = 1; i <= 9; i++) soma += parseInt(cpf.substring(i-1, i)) * (11 - i);
        resto = (soma * 10) % 11;
        if ((resto === 10) || (resto === 11)) resto = 0;
        if (resto !== parseInt(cpf.substring(9, 10))) return false;
        soma = 0;
        for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i-1, i)) * (12 - i);
        resto = (soma * 10) % 11;
        if ((resto === 10) || (resto === 11)) resto = 0;
        if (resto !== parseInt(cpf.substring(10, 11))) return false;
        return true;
    }
    document.addEventListener('DOMContentLoaded', function() {
        // Validação de CPF
        var cpfInput = document.getElementById('cpf');
        if (cpfInput) {
            cpfInput.addEventListener('blur', function() {
                var val = cpfInput.value;
                if (val && !validarCPF(val)) {
                    cpfInput.setCustomValidity('Digite um CPF válido');
                    cpfInput.reportValidity();
                } else {
                    cpfInput.setCustomValidity('');
                }
            });
        }
        // Validação de e-mail
        var emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                var val = emailInput.value;
                var re = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
                if (val && !re.test(val)) {
                    emailInput.setCustomValidity('Digite um e-mail válido');
                    emailInput.reportValidity();
                } else {
                    emailInput.setCustomValidity('');
                }
            });
        }
    });
    </script>
    <header class="main-header">
        <div class="header-logos">
            <img src="/static/logo_fgm.png" alt="Logo FGM" class="logo">
            <img src="/static/logo-prefeitura.png" alt="Prefeitura do Rio" class="logo-prefeitura-topo">
        </div>
    </header>
    <main>
        <section id="hero" class="hero-section" style="background: linear-gradient(120deg, #fff 60%, #de254b 100%); border-radius: 24px; box-shadow: 0 4px 24px rgba(222,37,75,0.08); padding: 36px 0 32px 0; margin-bottom: 32px;">
            <div style="text-align:center; margin-bottom: 18px;">
                <span style="background: #de254b; color: #fff; font-weight: bold; font-size: 1.05em; padding: 8px 24px; border-radius: 24px; letter-spacing: 1px; box-shadow: 0 2px 8px #de254b22; display: inline-block;">PROJETO:<br>DANÇANDO NA PRAÇA</span>
            </div>
            <h1 style="font-size:2em; font-weight:900; text-align:center; margin-bottom: 10px; text-shadow: 0 2px 8px #fff, 0 1px 0 #de254b22; color:#de254b;">AULÃO DE DANÇA!</h1>
            <h2 style="font-size:1em; font-weight:400; color:#de254b; text-align:center; margin-bottom: 22px;">Evento Gratuito: Aulão de Forró, Gafieira e Samba no Pé com Prof. Stefany<br>📍 Parque Poeta Manuel Bandeira, s/n, Aterro do Cocotá, Ilha do Governador, RJ. (ANFITEATRO)</h2>
            <div class="benefits" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 24px; margin-top: 18px;">
                <div class="benefit-carousel" style="display: flex; justify-content: center; align-items: center; margin-top: 24px; width: 100%;">
                    <div id="benefit-card" class="benefit" style="width: 100%; max-width: 700px; min-height: 80px; font-size: 1.25em; padding: 32px 32px; background: linear-gradient(90deg, #fff 80%, #eaf2fb 100%); border: 2px solid #de254b; border-radius: 22px; box-shadow: 0 4px 24px #de254b22; color: #de254b; font-weight: bold; text-align: center; transition: background 0.3s, box-shadow 0.3s, opacity 0.5s; opacity: 1;">
                        22/03 ÀS 17h, DOMINGO
                    </div>
                </div>
                <script>
                    const benefits = [
                        "22/03 ÀS 17h, DOMINGO",
                        "EVENTO GRATUITO",
                        "AULÃO DE RITMOS",
                        "EM CASO DE CHUVA SERÁ CANCELADO",
                        "VAGAS LIMITADAS, GARANTA A SUA"
                    ];
                    let benefitIndex = 0;
                    setInterval(() => {
                        const card = document.getElementById('benefit-card');
                        card.style.opacity = 0;
                        setTimeout(() => {
                            benefitIndex = (benefitIndex + 1) % benefits.length;
                            card.textContent = benefits[benefitIndex];
                            card.style.opacity = 1;
                        }, 500);
                    }, 3000);
                </script>
            </div>
        </section>
        <div style="text-align:center;">
            <a href="/inscricao" class="cta-btn">INSCREVER ME!</a>
        </div>
        <section id="cursos" class="cursos-section">
            <p class="cursos-title">RITMOS</p>
            <p class="cursos-destaque"><b>FORRÓ</b> &bull; <b>GAFIEIRA</b> &bull; <b>SAMBA NO PÉ</b></p>
        </section>
        <!-- Seção de ganhos removida pois os benefícios já estão destacados acima -->
        <section id="contato" class="contato-section">
            
            <img src="https://investidordesucesso.fgmcursos.com.br/assets/logo-rj-C4on5mTt.png" alt="Prefeitura do Rio de Janeiro" class="logo-prefeitura">
        </section>
    </main>
    <footer style="border-top: 4px solid #de254b; background: linear-gradient(90deg, #fff 60%, #de254b 100%);">
        <p style="color: #de254b;">&copy; 2020 FGM. Todos os direitos Reservados</p>
    </footer>
</body>
</html>
'''

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'  # Troque por uma chave forte em produção

@app.route('/')
def home():
    return render_template_string(TEMPLATE_INDEX)

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        from datetime import datetime
        nome = request.form.get('nome', '')
        if len(nome) > 50:
            return render_template_string(TEMPLATE_INSCRICAO, erro_nome='O nome deve ter no máximo 50 caracteres.')
        session['nome'] = nome
        session['cpf'] = request.form.get('cpf')
        nascimento = request.form.get('nascimento')
        session['nascimento'] = nascimento
        whatsapp = request.form.get('whatsapp','')
        import re
        ddd_match = re.match(r'\((\d{2})\)', whatsapp)
        ddd = ddd_match.group(1) if ddd_match else None
        ddds_validos = [
            '68','96','92','97','91','93','94','95','63','69', # Norte
            '82','71','73','74','75','77','85','88','98','99','83','81','87','86','89','84','79', # Nordeste
            '61','62','64','65','66','67', # Centro-Oeste
            '27','28','31','32','33','34','35','37','38','21','22','24','11','12','13','14','15','16','17','18','19', # Sudeste
            '41','42','43','44','45','46','47','48','49','51','53','54','55' # Sul
        ]
        if not ddd or ddd not in ddds_validos:
            return render_template_string(TEMPLATE_INSCRICAO, erro_whatsapp='Informe um DDD válido do Brasil.')
        session['whatsapp'] = whatsapp
        session['email'] = request.form.get('email')
        session['genero'] = request.form.get('genero')
        # Validação de idade mínima e máxima
        try:
            if nascimento:
                # Aceita tanto yyyy-mm-dd (formulário HTML) quanto dd/mm/yyyy (usuário)
                if '-' in nascimento:
                    data_nasc = datetime.strptime(nascimento, '%Y-%m-%d')
                else:
                    data_nasc = datetime.strptime(nascimento, '%d/%m/%Y')
                hoje = datetime.today()
                idade = (hoje - data_nasc).days // 365
                if idade > 90:
                    return render_template_string(TEMPLATE_INSCRICAO, erro_nascimento='Idade permitida: de 16 até 90 anos')
                if idade < 16:
                    return render_template_string(TEMPLATE_INSCRICAO, erro_nascimento='Idade permitida: de 16 até 90 anos')
        except Exception:
            return render_template_string(TEMPLATE_INSCRICAO, erro_nascimento='Data de nascimento inválida.')
        return redirect(url_for('curso'))
    return render_template_string(TEMPLATE_INSCRICAO)

@app.route('/endereco', methods=['GET', 'POST'])
def endereco():
    if request.method == 'POST':
        cep = request.form.get('cep', '').replace('-', '').strip()
        if not (cep.isdigit() and len(cep) == 8):
            return render_template_string(TEMPLATE_ENDERECO, erro_cep='CEP inválido. Informe no formato 00000-000.')
        session['cep'] = request.form.get('cep')
        session['endereco'] = request.form.get('endereco')
        session['numero'] = request.form.get('numero')
        session['complemento'] = request.form.get('complemento')
        session['bairro'] = request.form.get('bairro')
        session['cidade'] = request.form.get('cidade')
        session['estado'] = request.form.get('estado')
        return redirect(url_for('curso'))
    return render_template_string(TEMPLATE_ENDERECO)

@app.route('/curso', methods=['GET', 'POST'])
def curso():
    if request.method == 'POST':
        session['local'] = request.form.get('local')
        session['curso'] = request.form.get('curso')
        session['turma'] = request.form.get('turma')
        session['horario'] = request.form.get('horario')
        session['data_inicio'] = request.form.get('data_inicio')
        session['encerramento'] = request.form.get('encerramento')
        session['endereco_curso'] = request.form.get('endereco')
        return redirect(url_for('revisao'))
    return render_template_string(TEMPLATE_CURSO)

@app.route('/revisao', methods=['GET', 'POST'])
def revisao():
    if request.method == 'POST':
        session['como_conheceu'] = request.form.get('como_conheceu')
        return redirect(url_for('confirmacao'))
    return render_template_string(TEMPLATE_REVISAO, dados=session)

@app.route('/confirmacao')
def confirmacao():
    # Gera protocolo único
    protocolo = str(uuid.uuid4())[:8]
    session['protocolo'] = protocolo
    dados = [
        protocolo,
        session.get('nome',''),
        session.get('genero',''),
        session.get('cpf',''),
        session.get('nascimento',''),
        session.get('whatsapp',''),
        session.get('email',''),
        session.get('cep',''),
        session.get('bairro',''),
        session.get('local',''),
        session.get('curso',''),
        session.get('turma',''),
        session.get('horario',''),
        session.get('data_inicio',''),
        session.get('encerramento',''),
        session.get('endereco_curso',''),
        session.get('como_conheceu',''),
    ]
    # O campo data_envio será adicionado por append_to_sheet
    try:
        append_to_sheet(dados)
    except Exception as e:
        print('Erro ao salvar na planilha:', e)
        traceback.print_exc()
    return render_template_string(TEMPLATE_CONFIRMACAO, protocolo=protocolo)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
