#!/usr/bin/env bash
# Recria os 4 projetos de teste em evals/fixtures/ (spring, python, skillproj, vazio).
set -euo pipefail
E=$(cd "$(dirname "$0")" && pwd)
F=$E/fixtures
[ -e "$F" ] && { echo "evals/fixtures já existe; apague à mão para recriar"; exit 1; }
mkdir -p "$F/vazio"

# ---------- spring: Spring Boot 3.3.5 / Java 21 ----------
P=$F/spring; J=$P/src/main/java/com/exemplo/loja; T=$P/src/test/java/com/exemplo/loja
mkdir -p $J/{controller,service,model,repository} $T/service $P/src/main/resources
cat > $P/pom.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <parent><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-parent</artifactId><version>3.3.5</version></parent>
  <groupId>com.exemplo</groupId><artifactId>loja</artifactId><version>0.1.0</version>
  <properties><java.version>21</java.version></properties>
  <dependencies>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-security</artifactId></dependency>
    <dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId><scope>runtime</scope></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
    <dependency><groupId>junit</groupId><artifactId>junit</artifactId><version>4.13.2</version><scope>test</scope></dependency>
    <dependency><groupId>org.junit.vintage</groupId><artifactId>junit-vintage-engine</artifactId><scope>test</scope></dependency>
  </dependencies>
</project>
EOF
cat > $P/CLAUDE.md <<'EOF'
# loja
- Build e testes: `./mvnw test`
- Camadas: controller -> service -> repository. Controllers recebem e devolvem DTOs (records em `dto/`).
- Banco: PostgreSQL 16; migrations ainda não existem (ddl-auto=update).
EOF
printf '#!/bin/sh\nexec mvn "$@"\n' > $P/mvnw; chmod +x $P/mvnw
printf 'spring.jpa.open-in-view=false\nspring.jpa.hibernate.ddl-auto=update\nspring.datasource.url=jdbc:postgresql://localhost:5432/loja\n' > $P/src/main/resources/application.properties
cat > $J/model/Cliente.java <<'EOF'
package com.exemplo.loja.model;
import jakarta.persistence.*;
@Entity
public class Cliente {
  @Id @GeneratedValue Long id;
  String nome;
  String email; // sem unique: há duplicados em produção
  String senha;
  public Long getId() { return id; } public String getEmail() { return email; } public String getSenha() { return senha; }
}
EOF
cat > $J/model/Pedido.java <<'EOF'
package com.exemplo.loja.model;
import jakarta.persistence.*; import java.util.*;
@Entity
public class Pedido {
  @Id @GeneratedValue Long id;
  @ManyToOne Cliente cliente;
  @OneToMany(mappedBy = "pedido") List<ItemPedido> itens = new ArrayList<>();
  public Long getId() { return id; } public Cliente getCliente() { return cliente; } public List<ItemPedido> getItens() { return itens; }
}
EOF
cat > $J/model/ItemPedido.java <<'EOF'
package com.exemplo.loja.model;
import jakarta.persistence.*; import java.math.BigDecimal;
@Entity
public class ItemPedido {
  @Id @GeneratedValue Long id;
  @ManyToOne Pedido pedido;
  String produto; int quantidade; BigDecimal preco;
}
EOF
cat > $J/repository/PedidoRepository.java <<'EOF'
package com.exemplo.loja.repository;
import com.exemplo.loja.model.Pedido; import org.springframework.data.jpa.repository.JpaRepository; import java.util.List;
public interface PedidoRepository extends JpaRepository<Pedido, Long> { List<Pedido> findByClienteId(Long clienteId); }
EOF
cat > $J/repository/ClienteRepository.java <<'EOF'
package com.exemplo.loja.repository;
import com.exemplo.loja.model.Cliente; import org.springframework.data.jpa.repository.JpaRepository; import java.util.Optional;
public interface ClienteRepository extends JpaRepository<Cliente, Long> { Optional<Cliente> findFirstByEmail(String email); }
EOF
cat > $J/service/PedidoService.java <<'EOF'
package com.exemplo.loja.service;
import com.exemplo.loja.model.Pedido; import com.exemplo.loja.repository.PedidoRepository; import org.springframework.stereotype.Service;
@Service
public class PedidoService {
  private final PedidoRepository repo;
  public PedidoService(PedidoRepository repo) { this.repo = repo; }
  public Pedido buscar(Long id) { return repo.findById(id).orElseThrow(); }
}
EOF
cat > $J/controller/PedidoController.java <<'EOF'
package com.exemplo.loja.controller;
import com.exemplo.loja.model.Pedido; import com.exemplo.loja.service.PedidoService; import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/pedidos")
public class PedidoController {
  private final PedidoService service;
  public PedidoController(PedidoService service) { this.service = service; }
  @GetMapping("/{id}") public Pedido buscar(@PathVariable Long id) { return service.buscar(id); } // devolve a entidade (itens LAZY)
}
EOF
cat > $J/controller/AuthController.java <<'EOF'
package com.exemplo.loja.controller;
import com.exemplo.loja.repository.ClienteRepository; import org.springframework.web.bind.annotation.*; import java.util.*;
@RestController @RequestMapping("/auth")
public class AuthController {
  private final ClienteRepository clientes;
  public AuthController(ClienteRepository clientes) { this.clientes = clientes; }
  @PostMapping("/login")
  public Map<String, String> login(@RequestParam String email, @RequestParam String senha) {
    var c = clientes.findFirstByEmail(email).orElseThrow(() -> new RuntimeException("usuario " + email + " nao existe"));
    if (!c.getSenha().equals(senha)) throw new RuntimeException("senha errada");
    return Map.of("token", Base64.getEncoder().encodeToString((email + ":" + System.currentTimeMillis()).getBytes()));
  }
}
EOF
cat > $T/service/PedidoServiceTest.java <<'EOF'
package com.exemplo.loja.service;
import org.junit.Test; import org.junit.Before; import static org.junit.Assert.*; import static org.mockito.Mockito.*;
import com.exemplo.loja.repository.PedidoRepository; import com.exemplo.loja.model.Pedido; import java.util.Optional;
public class PedidoServiceTest {
  PedidoRepository repo; PedidoService service;
  @Before public void setUp() { repo = mock(PedidoRepository.class); service = new PedidoService(repo); }
  @Test public void buscaPedido() { when(repo.findById(1L)).thenReturn(Optional.of(new Pedido())); assertNotNull(service.buscar(1L)); }
  @Test(expected = java.util.NoSuchElementException.class) public void pedidoInexistente() { service.buscar(9L); }
}
EOF

# ---------- python: Python 3.12 / pytest ----------
Q=$F/python; mkdir -p $Q/src/fretes $Q/tests $Q/logs
cat > $Q/pyproject.toml <<'EOF'
[project]
name = "fretes"
version = "0.3.0"
requires-python = ">=3.12"
dependencies = ["requests>=2.32"]
[project.optional-dependencies]
dev = ["pytest>=8"]
[tool.pytest.ini_options]
testpaths = ["tests"]
EOF
cat > $Q/src/fretes/frete.py <<'EOF'
import sqlite3

TABELA = {"SP": 10.0, "RJ": 12.5, "MG": 11.0}

def calcula_frete(uf, peso_kg, cupom=None):
    base = TABELA[uf]
    total = base + peso_kg * 2
    if cupom:
        conn = sqlite3.connect("fretes.db")
        row = conn.execute(f"SELECT desconto FROM cupons WHERE codigo = '{cupom}'").fetchone()
        total = total - row[0]
    return round(total, 2)
EOF
cat > $Q/src/fretes/relatorio.py <<'EOF'
import json

def gera_relatorio(caminho):
    try:
        pedidos = json.load(open(caminho))
    except:
        return {}
    soma = 0
    for p in pedidos:
        soma += p["total"]
    return {"qtd": len(pedidos), "soma": soma, "media": soma / len(pedidos)}
EOF
cat > $Q/tests/test_frete.py <<'EOF'
from fretes.frete import calcula_frete

def test_sp():
    assert calcula_frete("SP", 1) == 12.0
EOF
python3 -I - "$Q/logs/app.log" <<'EOF'
import random, sys
random.seed(1); L = []
for h in range(8, 20):
    for i in range(40):
        ms = random.randint(80, 250) + (random.randint(900, 2500) if 13 <= h <= 16 and i % 3 == 0 else 0)
        L.append(f"2026-11-09T{h:02d}:{i:02d}:{random.randint(0,59):02d} INFO GET /fretes/calcular status=200 dur_ms={ms}")
open(sys.argv[1], 'w').write("\n".join(L) + "\n")
EOF

# ---------- skillproj: cópia da skill v1 ----------
K=$F/skillproj; mkdir -p $K; cp -r "$E/fixture-sources/skill-v1/." $K/

for d in $P $Q $K; do (cd $d && git init -q && git add -A && git -c user.name=fx -c user.email=fx@exemplo.invalid commit -qm "estado inicial"); done
echo "fixtures criadas em $F"
