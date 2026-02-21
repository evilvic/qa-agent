<script setup>
import { ref } from 'vue'
import StatusBadge from '@/components/StatusBadge.vue'
import VerdictCard from '@/components/VerdictCard.vue'
import RunButton from '@/components/RunButton.vue'
import EmptyState from '@/components/EmptyState.vue'
import RunningIndicator from '@/components/RunningIndicator.vue'
import TechnicalDetails from '@/components/TechnicalDetails.vue'
import TestRow from '@/components/TestRow.vue'
import TestForm from '@/components/TestForm.vue'
import ProjectSelector from '@/components/ProjectSelector.vue'

const showRunning = ref(true)

const mockProjects = [
  { id: '1', name: 'Mi tienda online' },
  { id: '2', name: 'API de pagos' },
  { id: '3', name: 'App móvil staging' },
]
</script>

<template>
  <div class="guide">
    <header class="guide__header">
      <h1 class="guide__title">Sistema de experiencia</h1>
      <p class="guide__subtitle">
        Guía viva del producto de QA Agent. Los componentes de esta página son los mismos que usa la aplicación.
        Cada sección explica las decisiones de diseño y muestra todos los estados posibles.
      </p>
    </header>

    <nav class="guide__nav">
      <a href="#colores">Colores</a>
      <a href="#tipografia">Tipografía</a>
      <a href="#espaciado">Espaciado</a>
      <a href="#componentes">Componentes</a>
      <a href="#journeys">Journeys</a>
      <a href="#copy">Copy</a>
    </nav>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- COLORES                                                        -->
    <!-- ════════════════════════════════════════════════════════════════ -->

    <section id="colores" class="guide__section">
      <h2>Paleta de colores</h2>
      <p class="guide__desc">
        Cada color tiene significado semántico fijo. Un verde <strong>siempre</strong> significa "pasó".
        No hay reinterpretación por contexto. Cada estado tiene 4 variantes: sólido, fondo, borde y texto.
      </p>

      <h3>Colores de estado</h3>
      <div class="swatches">
        <div class="swatch-group">
          <div class="swatch-group__label">Pass</div>
          <div class="swatch" style="background: var(--color-pass)"><span>#22c55e</span></div>
          <div class="swatch swatch--light" style="background: var(--color-pass-bg); border-color: var(--color-pass-border)"><span>bg</span></div>
          <div class="swatch swatch--light" style="background: var(--color-pass-border)"><span>border</span></div>
          <div class="swatch" style="background: var(--color-pass-text)"><span>text</span></div>
        </div>
        <div class="swatch-group">
          <div class="swatch-group__label">Fail</div>
          <div class="swatch" style="background: var(--color-fail)"><span>#ef4444</span></div>
          <div class="swatch swatch--light" style="background: var(--color-fail-bg); border-color: var(--color-fail-border)"><span>bg</span></div>
          <div class="swatch swatch--light" style="background: var(--color-fail-border)"><span>border</span></div>
          <div class="swatch" style="background: var(--color-fail-text)"><span>text</span></div>
        </div>
        <div class="swatch-group">
          <div class="swatch-group__label">Error</div>
          <div class="swatch" style="background: var(--color-error)"><span>#f59e0b</span></div>
          <div class="swatch swatch--light" style="background: var(--color-error-bg); border-color: var(--color-error-border)"><span>bg</span></div>
          <div class="swatch swatch--light" style="background: var(--color-error-border)"><span>border</span></div>
          <div class="swatch" style="background: var(--color-error-text)"><span>text</span></div>
        </div>
        <div class="swatch-group">
          <div class="swatch-group__label">Running</div>
          <div class="swatch" style="background: var(--color-running)"><span>#3b82f6</span></div>
          <div class="swatch swatch--light" style="background: var(--color-running-bg); border-color: var(--color-running-border)"><span>bg</span></div>
          <div class="swatch swatch--light" style="background: var(--color-running-border)"><span>border</span></div>
          <div class="swatch" style="background: var(--color-running-text)"><span>text</span></div>
        </div>
        <div class="swatch-group">
          <div class="swatch-group__label">Neutro</div>
          <div class="swatch" style="background: var(--color-neutral)"><span>#6b7280</span></div>
          <div class="swatch swatch--light" style="background: var(--color-neutral-bg); border-color: var(--color-neutral-border)"><span>bg</span></div>
          <div class="swatch swatch--light" style="background: var(--color-neutral-border)"><span>border</span></div>
          <div class="swatch" style="background: var(--color-neutral-text)"><span>text</span></div>
        </div>
      </div>

      <h3>Superficies y texto</h3>
      <div class="swatches">
        <div class="swatch-group">
          <div class="swatch-group__label">Superficies</div>
          <div class="swatch swatch--light" style="background: var(--surface-page); border: 1px solid #e5e7eb"><span>page</span></div>
          <div class="swatch swatch--light" style="background: var(--surface-section)"><span>section</span></div>
          <div class="swatch swatch--light" style="background: var(--border-default)"><span>border</span></div>
        </div>
        <div class="swatch-group">
          <div class="swatch-group__label">Texto</div>
          <div class="swatch" style="background: var(--text-primary)"><span>primary</span></div>
          <div class="swatch" style="background: var(--text-secondary)"><span>secondary</span></div>
          <div class="swatch swatch--light" style="background: var(--text-disabled); color: #fff"><span>disabled</span></div>
        </div>
        <div class="swatch-group">
          <div class="swatch-group__label">Acción</div>
          <div class="swatch" style="background: var(--action-primary)"><span>primary</span></div>
          <div class="swatch" style="background: var(--action-primary-hover)"><span>hover</span></div>
          <div class="swatch" style="background: var(--action-primary-active)"><span>active</span></div>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- TIPOGRAFÍA                                                     -->
    <!-- ════════════════════════════════════════════════════════════════ -->

    <section id="tipografia" class="guide__section">
      <h2>Tipografía</h2>
      <p class="guide__desc">
        System font stack. Sin tipografías externas que cargar. El tamaño base es 14px para densidad media.
        Lectura principal a 16px. Metadata y labels a 12px.
      </p>

      <div class="type-scale">
        <div class="type-sample" style="font-size: var(--font-size-2xl); font-weight: var(--font-weight-bold)">
          24px / Bold — Títulos principales
        </div>
        <div class="type-sample" style="font-size: var(--font-size-xl); font-weight: var(--font-weight-bold)">
          20px / Bold — Veredicto (Pasó / Falló)
        </div>
        <div class="type-sample" style="font-size: var(--font-size-lg); font-weight: var(--font-weight-semibold)">
          18px / Semibold — Títulos de sección
        </div>
        <div class="type-sample" style="font-size: var(--font-size-base)">
          16px / Normal — Lectura principal, razón del veredicto
        </div>
        <div class="type-sample" style="font-size: var(--font-size-sm)">
          14px / Normal — Texto base, formularios, listas
        </div>
        <div class="type-sample" style="font-size: var(--font-size-sm); font-weight: var(--font-weight-medium)">
          14px / Medium — Labels, nombres de tests
        </div>
        <div class="type-sample" style="font-size: var(--font-size-xs); color: var(--text-secondary)">
          12px / Normal — Metadata, timestamps, helper text
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- ESPACIADO                                                      -->
    <!-- ════════════════════════════════════════════════════════════════ -->

    <section id="espaciado" class="guide__section">
      <h2>Espaciado</h2>
      <p class="guide__desc">
        Escala basada en múltiplos de 4px. Consistencia espacial genera ritmo visual.
        El contenido máximo es 960px (no 1200 — los tests no necesitan tanto ancho).
      </p>

      <div class="spacing-scale">
        <div v-for="[name, size] in [['space-1', '4px'], ['space-2', '8px'], ['space-3', '12px'], ['space-4', '16px'], ['space-6', '24px'], ['space-8', '32px'], ['space-12', '48px']]" :key="name" class="spacing-item">
          <div class="spacing-block" :style="{ width: size, height: size }"></div>
          <code>--{{ name }}</code>
          <span class="spacing-value">{{ size }}</span>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- COMPONENTES                                                    -->
    <!-- ════════════════════════════════════════════════════════════════ -->

    <section id="componentes" class="guide__section">
      <h2>Componentes</h2>
      <p class="guide__desc">
        Componentes reales de Vue. Cada uno encapsula comportamiento, estados y accesibilidad.
        Los mismos archivos <code>.vue</code> que se usarán en la aplicación.
      </p>

      <!-- StatusBadge -->
      <div class="component-showcase">
        <h3>StatusBadge</h3>
        <p>Indicador del estado de un run. Un badge verde siempre significa "pasó". Reutilizable en toda la app.</p>
        <div class="component-demo">
          <StatusBadge status="pass" />
          <StatusBadge status="fail" />
          <StatusBadge status="error" />
          <StatusBadge status="running" />
          <StatusBadge status="none" />
        </div>
      </div>

      <!-- VerdictCard -->
      <div class="component-showcase">
        <h3>VerdictCard</h3>
        <p>El momento de verdad. Lo primero que el usuario ve después de un run. Borde izquierdo grueso, texto grande, sin ambigüedad.</p>
        <div class="component-demo component-demo--stack">
          <VerdictCard
            status="pass"
            reason="El login fue exitoso. Se llegó al dashboard y el nombre del usuario es visible en la barra superior."
          />
          <VerdictCard
            status="fail"
            reason="No se encontró el dashboard después del login. La página muestra un error 404 en la ruta /dashboard."
          />
          <VerdictCard
            status="error"
            reason="Timeout después de 120 segundos. El agente no pudo completar la navegación."
          />
        </div>
      </div>

      <!-- RunButton -->
      <div class="component-showcase">
        <h3>RunButton</h3>
        <p>Dispara la ejecución. Tres estados: listo, en progreso, deshabilitado. Versión completa y compacta (para listas).</p>
        <div class="component-demo">
          <RunButton state="idle" />
          <RunButton state="running" />
          <RunButton state="disabled" />
        </div>
        <div class="component-demo" style="margin-top: var(--space-3)">
          <span style="font-size: var(--font-size-xs); color: var(--text-secondary)">Compacto:</span>
          <RunButton state="idle" compact />
          <RunButton state="running" compact />
          <RunButton state="disabled" compact />
        </div>
      </div>

      <!-- TestRow -->
      <div class="component-showcase">
        <h3>TestRow</h3>
        <p>Fila de la lista de tests. Muestra badge, nombre, metadata y botón de ejecución. Click lleva al detalle.</p>
        <div class="component-demo component-demo--stack" style="max-width: 600px">
          <TestRow name="Login con credenciales válidas" status="pass" lastRun="Hace 2 horas" />
          <TestRow name="Navegación al catálogo de productos" status="fail" lastRun="Hace 15 minutos" />
          <TestRow name="Checkout con tarjeta de crédito" status="error" lastRun="Ayer" />
          <TestRow name="Registro de nuevo usuario" status="none" />
          <TestRow name="Buscar producto por nombre" running lastRun="Ahora" />
        </div>
      </div>

      <!-- TestForm -->
      <div class="component-showcase">
        <h3>TestForm</h3>
        <p>Formulario inline para crear o editar tests. Tres campos porque cada uno tiene un propósito: nombre (identificar), instrucciones (para el agente), resultado esperado (para el veredicto).</p>
        <div class="component-demo component-demo--stack" style="max-width: 600px">
          <TestForm />
        </div>
        <p style="margin-top: var(--space-3); font-size: var(--font-size-xs); color: var(--text-secondary)">
          Arriba: formulario vacío (crear). Abajo: pre-poblado (editar).
        </p>
        <div class="component-demo component-demo--stack" style="max-width: 600px; margin-top: var(--space-3)">
          <TestForm
            initialName="Login con credenciales válidas"
            initialInstructions="Inicia sesión con las credenciales del proyecto y navega al dashboard principal."
            initialExpected="El dashboard se muestra con el nombre del usuario visible en la barra superior."
          />
        </div>
      </div>

      <!-- EmptyState -->
      <div class="component-showcase">
        <h3>EmptyState</h3>
        <p>Cada estado vacío es una invitación, no un error. Guía al usuario hacia la siguiente acción con copy claro y un CTA.</p>
        <div class="component-demo component-demo--stack" style="background: var(--surface-section); border-radius: var(--radius-lg)">
          <EmptyState
            title="No hay pruebas todavía"
            description="Crea tu primera prueba para empezar a validar tu aplicación."
            actionLabel="Crear prueba"
          />
        </div>
        <div class="component-demo component-demo--stack" style="background: var(--surface-section); border-radius: var(--radius-lg); margin-top: var(--space-3)">
          <EmptyState
            title="Sin ejecuciones"
            description="Esta prueba no se ha ejecutado. Haz click en Ejecutar para correrla."
            actionLabel="Ejecutar ahora"
          />
        </div>
      </div>

      <!-- RunningIndicator -->
      <div class="component-showcase">
        <h3>RunningIndicator</h3>
        <p>Barra fija inferior durante un run. Reduce ansiedad mostrando que algo pasa. Incluye timer y link para navegar al test.</p>
        <div class="component-demo" style="position: relative; min-height: 60px; overflow: hidden; border-radius: var(--radius-lg)">
          <div style="position: absolute; bottom: 0; left: 0; right: 0; background: var(--color-running-bg); border-top: 1px solid var(--color-running-border); padding: var(--space-3) var(--space-4);">
            <div style="display: flex; align-items: center; gap: var(--space-3); font-size: var(--font-size-sm); color: var(--color-running-text);">
              <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--color-running); animation: pulse 1.5s ease-in-out infinite;"></span>
              <span>Ejecutando <strong>"Login exitoso"</strong> — 23s</span>
              <button style="margin-left: auto; background: none; border: 1px solid var(--color-running-border); border-radius: var(--radius-md); padding: 2px var(--space-3); color: var(--color-running-text); font-size: var(--font-size-xs); cursor: pointer;">Ver</button>
            </div>
          </div>
        </div>
        <p style="margin-top: var(--space-2); font-size: var(--font-size-xs); color: var(--text-secondary)">
          Vista demo inline. En la app real, esta barra se fija al fondo de la ventana.
        </p>
      </div>

      <!-- TechnicalDetails -->
      <div class="component-showcase">
        <h3>TechnicalDetails</h3>
        <p>Información técnica colapsada por defecto. Lo técnico se esconde hasta que se necesita. Click para expandir.</p>
        <div class="component-demo component-demo--stack" style="max-width: 600px">
          <TechnicalDetails
            model="gpt-4.1-mini"
            :tokens="2340"
            :duration="34.2"
            url="https://app.ejemplo.com/dashboard"
            runId="20260221_143200_a1b2c3d4"
          />
        </div>
      </div>

      <!-- ProjectSelector -->
      <div class="component-showcase">
        <h3>ProjectSelector</h3>
        <p>Dropdown para cambiar de workspace. El proyecto es contexto global, no navegación. Siempre visible en la barra superior.</p>
        <div class="component-demo" style="min-height: 200px">
          <ProjectSelector
            :projects="mockProjects"
            activeId="1"
          />
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- JOURNEYS                                                       -->
    <!-- ════════════════════════════════════════════════════════════════ -->

    <section id="journeys" class="guide__section">
      <h2>Journeys del usuario</h2>
      <p class="guide__desc">
        Los 6 flujos principales del MVP. Cada uno es una secuencia de momentos con trigger, acción y resultado.
        El producto se experimenta como estas narrativas, no como pantallas sueltas.
      </p>

      <div class="journey">
        <h3>1. Configurar mi primera app</h3>
        <div class="journey__flow">
          <div class="journey__step journey__step--trigger">
            <div class="journey__step-label">Trigger</div>
            Primera vez, sin proyectos
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">Estado vacío</div>
            "Configura tu primera app"
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">Formulario</div>
            Nombre, URL, credenciales
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step journey__step--result">
            <div class="journey__step-label">Resultado</div>
            Proyecto activo, lista de tests vacía
          </div>
        </div>
      </div>

      <div class="journey">
        <h3>2. Crear un test</h3>
        <div class="journey__flow">
          <div class="journey__step journey__step--trigger">
            <div class="journey__step-label">Trigger</div>
            Quiere probar algo
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">Acción</div>
            Click "+ Nueva prueba"
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">Formulario inline</div>
            Nombre, instrucciones, resultado esperado
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step journey__step--result">
            <div class="journey__step-label">Resultado</div>
            Test en la lista, listo para ejecutar
          </div>
        </div>
      </div>

      <div class="journey">
        <h3>3. Ejecutar un test</h3>
        <div class="journey__flow">
          <div class="journey__step journey__step--trigger">
            <div class="journey__step-label">Trigger</div>
            Click "Ejecutar"
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step journey__step--running">
            <div class="journey__step-label">Espera (10-120s)</div>
            Badge azul, timer, indicador
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step journey__step--result">
            <div class="journey__step-label">Resultado</div>
            PASÓ / FALLÓ / ERROR
          </div>
        </div>
        <p class="journey__note">
          <strong>Momento crítico:</strong> la espera. Sin feedback, 30 segundos se sienten como 5 minutos.
          El RunningIndicator y el timer reducen la ansiedad.
        </p>
      </div>

      <div class="journey">
        <h3>4. Ver resultado de un run</h3>
        <div class="journey__flow">
          <div class="journey__step journey__step--trigger">
            <div class="journey__step-label">Trigger</div>
            Run terminó o click en historial
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">1. Veredicto</div>
            Grande, claro, con color
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">2. Evidencia</div>
            Screenshots + pasos
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">3. Técnico</div>
            Colapsado (modelo, tokens)
          </div>
        </div>
        <p class="journey__note">
          <strong>Jerarquía no negociable:</strong> Veredicto → Razón → Evidencia → Técnico.
          El PoC mostraba esto al revés (IDs arriba, resultado abajo).
        </p>
      </div>

      <div class="journey">
        <h3>5. Revisar historial</h3>
        <div class="journey__flow">
          <div class="journey__step journey__step--trigger">
            <div class="journey__step-label">Trigger</div>
            Click en un test
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">Detalle del test</div>
            Info + botón ejecutar
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step journey__step--result">
            <div class="journey__step-label">Historial</div>
            Lista de runs con tendencia
          </div>
        </div>
      </div>

      <div class="journey">
        <h3>6. Cambiar de proyecto</h3>
        <div class="journey__flow">
          <div class="journey__step journey__step--trigger">
            <div class="journey__step-label">Trigger</div>
            Quiere probar otra app
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step">
            <div class="journey__step-label">Selector</div>
            Dropdown en barra superior
          </div>
          <div class="journey__arrow"></div>
          <div class="journey__step journey__step--result">
            <div class="journey__step-label">Resultado</div>
            Contexto cambia, tests actualizan
          </div>
        </div>
      </div>
    </section>

    <!-- ════════════════════════════════════════════════════════════════ -->
    <!-- COPY                                                           -->
    <!-- ════════════════════════════════════════════════════════════════ -->

    <section id="copy" class="guide__section">
      <h2>Sistema de copy</h2>
      <p class="guide__desc">
        El lenguaje es parte del sistema de experiencia. No se agrega después.
        Define cómo el producto se comunica y genera confianza.
      </p>

      <div class="copy-block">
        <h3>Voz del producto</h3>
        <ul class="copy-rules">
          <li><strong>Tuteo.</strong> El producto habla de "tú" al usuario. Es una herramienta profesional pero cercana, no corporativa.</li>
          <li><strong>Directo.</strong> Oraciones cortas. Verbos de acción. Sin rodeos ni adornos.</li>
          <li><strong>Español nativo.</strong> No es una traducción del inglés. Se dice "prueba", no "test". Se dice "ejecutar", no "correr". Excepciones: términos técnicos sin equivalente natural (dashboard, timeout, login).</li>
          <li><strong>Sin dramatismo.</strong> Los errores se reportan con calma. No hay exclamaciones en mensajes negativos.</li>
        </ul>
      </div>

      <div class="copy-block">
        <h3>Estados vacíos</h3>
        <p>Cada estado vacío guía al siguiente paso. Estructura: qué pasa + qué hacer.</p>
        <div class="copy-examples">
          <div class="copy-example copy-example--good">
            <div class="copy-example__label">Correcto</div>
            <p><strong>"No hay pruebas todavía."</strong></p>
            <p>"Crea tu primera prueba para empezar a validar tu aplicación."</p>
          </div>
          <div class="copy-example copy-example--bad">
            <div class="copy-example__label">Incorrecto</div>
            <p><strong>"No se encontraron tests!"</strong></p>
            <p>"Por favor, cree un test case para comenzar el proceso de QA."</p>
          </div>
        </div>
        <p class="copy-why">
          El correcto usa "pruebas" (español nativo), no dramatiza con "!", tutea, y da una acción clara.
          El incorrecto mezcla inglés, usa "usted", y suena a manual técnico.
        </p>
      </div>

      <div class="copy-block">
        <h3>Errores</h3>
        <p>Los errores explican qué pasó y (cuando es posible) qué hacer. Sin culpar al usuario.</p>
        <div class="copy-examples">
          <div class="copy-example copy-example--good">
            <div class="copy-example__label">Correcto</div>
            <p><strong>"Timeout después de 120 segundos."</strong></p>
            <p>"El agente no pudo completar la prueba a tiempo. Intenta simplificar las instrucciones o aumentar el límite."</p>
          </div>
          <div class="copy-example copy-example--bad">
            <div class="copy-example__label">Incorrecto</div>
            <p><strong>"ERROR: Agent execution timed out!"</strong></p>
            <p>"An unexpected error has occurred. Please try again later."</p>
          </div>
        </div>
      </div>

      <div class="copy-block">
        <h3>Confirmaciones</h3>
        <div class="copy-examples">
          <div class="copy-example copy-example--good">
            <div class="copy-example__label">Correcto</div>
            <p><strong>"Prueba creada."</strong></p>
            <p>"¿Seguro que quieres eliminar esta prueba? Esta acción no se puede deshacer."</p>
          </div>
          <div class="copy-example copy-example--bad">
            <div class="copy-example__label">Incorrecto</div>
            <p><strong>"¡Test guardado exitosamente!"</strong></p>
            <p>"¿Desea eliminar el test case seleccionado?"</p>
          </div>
        </div>
        <p class="copy-why">
          Confirmaciones positivas son breves. Confirmaciones destructivas son explícitas sobre la consecuencia.
          No se usa "exitosamente" (redundante si ya se confirma). No se usa "usted".
        </p>
      </div>

      <div class="copy-block">
        <h3>Placeholders</h3>
        <p>Los placeholders son ejemplos reales, no instrucciones genéricas.</p>
        <div class="copy-examples">
          <div class="copy-example copy-example--good">
            <div class="copy-example__label">Correcto</div>
            <p>placeholder: <em>"Login con credenciales válidas"</em></p>
            <p>placeholder: <em>"Inicia sesión con las credenciales del proyecto y navega al dashboard."</em></p>
          </div>
          <div class="copy-example copy-example--bad">
            <div class="copy-example__label">Incorrecto</div>
            <p>placeholder: <em>"Ingrese el nombre del test..."</em></p>
            <p>placeholder: <em>"Escriba las instrucciones aquí..."</em></p>
          </div>
        </div>
        <p class="copy-why">
          Los placeholders buenos muestran un ejemplo real de lo que se espera.
          Los malos repiten la etiqueta del campo. No aportan información nueva.
        </p>
      </div>

      <div class="copy-block">
        <h3>Glossario de términos</h3>
        <table class="copy-table">
          <thead>
            <tr><th>Usar</th><th>No usar</th><th>Por qué</th></tr>
          </thead>
          <tbody>
            <tr><td>Prueba</td><td>Test, test case</td><td>Español nativo</td></tr>
            <tr><td>Ejecutar</td><td>Correr, run</td><td>Verbo natural en español</td></tr>
            <tr><td>Ejecución</td><td>Run</td><td>Sustantivo natural</td></tr>
            <tr><td>Proyecto</td><td>Project, workspace</td><td>Español directo</td></tr>
            <tr><td>Pasó / Falló</td><td>Pass / Fail, Éxito / Falla</td><td>Natural, sin anglicismo, sin formalismo</td></tr>
            <tr><td>Resultado esperado</td><td>Expected outcome, assertion</td><td>Lenguaje humano</td></tr>
            <tr><td>Login</td><td>Inicio de sesión</td><td>Excepción: término técnico universal</td></tr>
            <tr><td>Dashboard</td><td>Panel, tablero</td><td>Excepción: término técnico universal</td></tr>
            <tr><td>Timeout</td><td>Tiempo de espera agotado</td><td>Excepción: término técnico reconocido</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Padding inferior para el RunningIndicator demo -->
    <div style="height: 80px"></div>

    <!-- RunningIndicator real (demo funcional) -->
    <RunningIndicator
      :visible="showRunning"
      testName="Login exitoso"
      :startTime="Date.now() - 23000"
      @navigate="showRunning = false"
    />
  </div>
</template>

<style scoped>
/* ─── Layout general del guide ─── */
.guide {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
}

.guide__header {
  margin-bottom: var(--space-8);
}

.guide__title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.guide__subtitle {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  max-width: 640px;
}

/* ─── Navegación ─── */
.guide__nav {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--border-default);
  margin-bottom: var(--space-8);
  flex-wrap: wrap;
}

.guide__nav a {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.guide__nav a:hover {
  color: var(--action-primary);
}

/* ─── Secciones ─── */
.guide__section {
  margin-bottom: var(--space-12);
}

.guide__section h2 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.guide__section h3 {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-top: var(--space-6);
  margin-bottom: var(--space-3);
}

.guide__desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--space-6);
  max-width: 640px;
}

.guide__desc code {
  font-size: var(--font-size-xs);
  background: var(--surface-section);
  padding: 1px var(--space-1);
  border-radius: var(--radius-sm);
}

/* ─── Swatches de color ─── */
.swatches {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
  margin-bottom: var(--space-6);
}

.swatch-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.swatch-group__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.swatch {
  width: 72px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: flex-end;
  padding: 2px 4px;
}

.swatch span {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: var(--font-weight-medium);
}

.swatch--light span {
  color: var(--text-secondary);
}

.swatch--light {
  border: 1px solid var(--border-default);
}

/* ─── Escala tipográfica ─── */
.type-scale {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.type-sample {
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--border-default);
}

/* ─── Escala de espaciado ─── */
.spacing-scale {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
  align-items: flex-end;
}

.spacing-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
}

.spacing-block {
  background: var(--action-primary);
  border-radius: 2px;
}

.spacing-item code {
  font-size: 10px;
  color: var(--text-primary);
}

.spacing-value {
  font-size: 10px;
  color: var(--text-secondary);
}

/* ─── Componentes showcase ─── */
.component-showcase {
  margin-bottom: var(--space-8);
  padding-bottom: var(--space-8);
  border-bottom: 1px solid var(--border-default);
}

.component-showcase:last-child {
  border-bottom: none;
}

.component-showcase p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--space-4);
  max-width: 640px;
}

.component-demo {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  align-items: flex-start;
  padding: var(--space-4);
  background: var(--surface-section);
  border-radius: var(--radius-lg);
  border: 1px dashed var(--border-default);
}

.component-demo--stack {
  flex-direction: column;
}

/* ─── Journeys ─── */
.journey {
  margin-bottom: var(--space-8);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--border-default);
}

.journey h3 {
  margin-top: 0;
}

.journey__flow {
  display: flex;
  align-items: center;
  gap: 0;
  flex-wrap: wrap;
  margin-bottom: var(--space-3);
}

.journey__step {
  padding: var(--space-3) var(--space-4);
  background: var(--surface-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-xs);
  color: var(--text-primary);
  min-width: 140px;
  text-align: center;
}

.journey__step-label {
  font-size: 10px;
  font-weight: var(--font-weight-semibold);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2px;
}

.journey__step--trigger {
  border-color: var(--color-neutral-border);
  background: var(--color-neutral-bg);
}

.journey__step--running {
  border-color: var(--color-running-border);
  background: var(--color-running-bg);
}

.journey__step--result {
  border-color: var(--color-pass-border);
  background: var(--color-pass-bg);
}

.journey__arrow {
  width: 24px;
  height: 2px;
  background: var(--border-default);
  position: relative;
  flex-shrink: 0;
}

.journey__arrow::after {
  content: '';
  position: absolute;
  right: 0;
  top: -3px;
  border: 4px solid transparent;
  border-left-color: var(--border-default);
}

.journey__note {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  padding: var(--space-3);
  background: var(--surface-section);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--color-running);
}

/* ─── Copy ─── */
.copy-block {
  margin-bottom: var(--space-8);
}

.copy-block h3 {
  margin-top: 0;
}

.copy-block > p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
}

.copy-rules {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.copy-rules li {
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
  padding-left: var(--space-4);
  border-left: 2px solid var(--border-default);
}

.copy-examples {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-3);
}

@media (max-width: 768px) {
  .copy-examples { grid-template-columns: 1fr; }
  .journey__flow { flex-direction: column; align-items: stretch; }
  .journey__arrow { width: 2px; height: 16px; margin: 0 auto; }
  .journey__arrow::after { right: -3px; top: auto; bottom: 0; border: 4px solid transparent; border-top-color: var(--border-default); border-left-color: transparent; }
}

.copy-example {
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  border: 1px solid;
  font-size: var(--font-size-sm);
}

.copy-example p {
  margin-bottom: var(--space-1);
}

.copy-example p:last-child {
  margin-bottom: 0;
}

.copy-example em {
  color: var(--text-secondary);
}

.copy-example--good {
  background: var(--color-pass-bg);
  border-color: var(--color-pass-border);
}

.copy-example--bad {
  background: var(--color-fail-bg);
  border-color: var(--color-fail-border);
}

.copy-example__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-2);
}

.copy-example--good .copy-example__label { color: var(--color-pass-text); }
.copy-example--bad .copy-example__label { color: var(--color-fail-text); }

.copy-why {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  padding: var(--space-3);
  background: var(--surface-section);
  border-radius: var(--radius-md);
}

.copy-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm);
}

.copy-table th {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  border-bottom: 2px solid var(--border-default);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  font-size: var(--font-size-xs);
}

.copy-table td {
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--border-default);
  color: var(--text-primary);
}

.copy-table td:nth-child(2) {
  color: var(--text-secondary);
  text-decoration: line-through;
}

.copy-table td:nth-child(3) {
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
}
</style>
