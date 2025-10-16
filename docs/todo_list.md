# To-Do List: Sistema de Urna Eletrônica Simplificada

## Planejamento
- [ ] Definir os integrantes do grupo (máximo 3 pessoas).
- [ ] Escolher a interface do usuário (modo texto ou gráfica).
- [x] Selecionar a linguagem de programação orientada a objetos (Django com SQLite3 já definido).

## Desenvolvimento
### Estrutura do Sistema
- [ ] Criar classes principais:
    - [ ] Classe `Candidato` (atributos: nome, número, cargo).
    - [ ] Classe `Votacao` (atributos: cargos, candidatos, votos).
    - [ ] Classe `Eleitor` (métodos para votar).
- [ ] Implementar conceitos de POO:
    - [ ] Encapsulamento.
    - [ ] Herança.
    - [ ] Polimorfismo.

### Funcionalidades
- [ ] Cadastro de Candidatos:
    - [ ] Permitir cadastro de candidatos com nome, número único e cargo.
- [ ] Cadastro da Votação:
    - [ ] Definir cargos disponíveis para a votação.
- [ ] Processo de Votação:
    - [ ] Validar número do candidato.
    - [ ] Registrar votos por cargo.
    - [ ] Permitir votos nulos e em branco.
- [ ] Contagem de Votos:
    - [ ] Registrar votos por candidato, nulos e em branco.
    - [ ] Implementar funcionalidade para resetar contadores para nova votação.
- [ ] Exibição de Resultados:
    - [ ] Listar total de votos por candidato.
    - [ ] Indicar vencedor por cargo.
- [ ] Persistência de Dados:
    - [ ] Salvar resultados em arquivo CSV compatível com Excel.

## Testes
- [ ] Testar cadastro de candidatos.
- [ ] Testar processo de votação (votos válidos, nulos e em branco).
- [ ] Testar contagem de votos e exibição de resultados.
- [ ] Testar persistência dos dados em CSV.

## Entrega
- [ ] Preparar apresentação para a aula.
- [ ] Garantir que o sistema esteja funcional e atenda aos requisitos.

## Extras (Opcional)
- [ ] Melhorar a interface do usuário.
- [ ] Adicionar validações extras para entrada de dados.
- [ ] Implementar logs para auditoria do processo de votação.