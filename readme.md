# 💰 Otimizando um Sistema Bancário com Programação Orientada a Objetos (POO) com Python

![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Este desafio é uma implementação de um **Sistema Bancário** desenvolvido em **Python**, seguindo o **Paradigma de Orientação a Objetos (POO)** e **Boas Práticas de Programação**.
O sistema permite criar usuários, abrir contas, realizar depósitos, saques, emitir extratos e consultar informações de forma interativa via terminal.

---

## 📌 Índice

- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Como Executar](#como-executar)
- [Autor](#autor)

---

<a id="funcionalidades"></a>

## 🧩 Funcionalidades

| Comando | Atividade          | Descrição                                                                 |
| ------- | ------------------ | ------------------------------------------------------------------------- |
| `d`     | Depositar          | Realiza depósitos em uma conta.                                           |
| `s`     | Sacar              | Efetua saques, validando saldo, limite e número máximo de saques diários. |
| `e`     | Extrato            | Exibe extrato de movimentações e saldo atual.                             |
| `nu`    | Novo usuário       | Cadastra um novo cliente do banco, validando CPF.                         |
| `lu`    | Listar usuários    | Lista todos os usuários cadastrados.                                      |
| `nc`    | Nova conta         | Cria uma nova conta vinculada a um usuário existente.                     |
| `lc`    | Listar contas      | Lista todas as contas cadastradas no sistema.                             |
| `lcu`   | Contas por usuário | Lista todas as contas vinculadas a um usuário pelo CPF.                   |
| `q`     | Sair               | Encerra o programa.                                                       |

---

<a id="estrutura-do-projeto"></a>

## 🏗 Estrutura do Projeto

O sistema é modularizado em funções:

- `depositar()` – depósitos (argumentos posicionais)
- `sacar()` – saques (keyword-only)
- `exibir_extrato()` – extrato (posicional + keyword)
- `validar_cpf()` – valida CPF
- `criar_usuario()` – cadastra novos usuários
- `listar_usuarios()` – lista usuários cadastrados
- `filtrar_usuario()` – busca usuário pelo CPF
- `criar_conta()` – cria conta bancária
- `listar_contas()` – lista todas as contas
- `listar_contas_por_usuario()` – lista contas de um usuário
- `main()` – função principal, gerencia o fluxo e menu

---

<a id="requisitos"></a>

## ⚙️ Requisitos

- Python 3.10 ou superior
- Nenhuma dependência externa (somente módulos da biblioteca padrão)

---

<a id="como-executar"></a>

## 🚀 Como Executar

1. Certifique-se de ter **Python 3.x** instalado.
2. Clone o repositório:

```bash
git clone https://github.com/duducavalcanti/trilha-python-dio-poo-desafio2.git
```

3. Acesse a pasta raiz do sistema:

```bash
cd sistema-bancario
```

4. Execute o arquivo do sistema:

```bash
python desafio_poo.py
```

<a id="autor"></a>

## 👤 Autor

Eduardo Cavalcanti
