import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def procesar_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path) as file:
            panel_texto.delete(1.0, tk.END)

            texto = file.read()
            count = 0
            inicio_programa_encontrado = False
            fin_programa_encontrado = False
            inicio_cuerpo_encontrado = False
            fin_cuerpo_encontrado = False
            errores = []
            program = texto.split("\n")
            for line in program:
                count += 1

                if line.strip() == "":
                    panel_texto.insert(tk.END, f"Línea {count} ignorada por estar vacía.\n")
                    panel_texto.insert(tk.END, "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _\n")
                    continue
                elif line.strip().startswith("//"):
                    panel_texto.insert(tk.END, f"Línea {count} ignorada por ser un comentario.\n")
                    panel_texto.insert(tk.END, "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _\n")
                    continue

                if line.strip().startswith("##"):
                    if not inicio_programa_encontrado:
                        inicio_programa_encontrado = True
                    else:
                        fin_programa_encontrado = True
                    panel_texto.insert(tk.END, f"Marca de inicio/fin de programa detectada en línea {count}.\n")
                    panel_texto.insert(tk.END, "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _\n")
                    continue
                elif line.strip() == "||":
                    if not inicio_cuerpo_encontrado:
                        inicio_cuerpo_encontrado = True
                    else:
                        fin_cuerpo_encontrado = True
                    panel_texto.insert(tk.END, f"Marca de inicio/fin de cuerpo detectada en línea {count}.\n")
                    panel_texto.insert(tk.END, "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _\n")
                    continue
                panel_texto.insert(tk.END, f"Línea #{count}: {line}\n")
                tokens = line.split(' ')
                token_encontrado = False
                es_tipo_variable = False
                es_nombre_variable = False
                esperando_igual = False
                valor_asignado = False
                for token in tokens:
                    if token in claves_variables:
                        es_tipo_variable = True
                        if es_tipo_variable:
                            if token not in claves_variables:
                                errores.append(f"Error en línea {count}: Tipo de variable desconocido '{token}'.")
                                continue
                            panel_texto.insert(tk.END, f"Tipo de variable: {token}\n")
                            es_tipo_variable = False
                            es_nombre_variable = True
                            continue
                    elif es_nombre_variable:
                        panel_texto.insert(tk.END, f"Nombre de la variable: {token}\n")
                        es_nombre_variable = False
                        esperando_igual = True
                        continue
                    elif esperando_igual:
                        if token != '=':
                            errores.append(f"Error en línea {count}: Se esperaba '=' después del nombre de la variable.")
                            break
                        esperando_igual = False
                        valor_asignado = True
                        continue
                    elif valor_asignado:
                        panel_texto.insert(tk.END, f"Valor asignado: {token}\n")
                        valor_asignado = False
                        continue
                    elif token in palabras_reservadas:
                        panel_texto.insert(tk.END, f"Palabra reservada detectada: {palabras_reservadas[token]}\n")
                        token_encontrado = True
                    elif token in claves_operadores:
                        panel_texto.insert(tk.END, f"El operador es: {operadores[token]}\n")
                        token_encontrado = True
                    elif token in claves_simbolos:
                        panel_texto.insert(tk.END, f"El símbolo de puntuación es: {simbolos[token]}\n")
                        token_encontrado = True
                    elif token.isdigit():
                        panel_texto.insert(tk.END, f"El token '{token}' es un número\n")
                        token_encontrado = True

                    if token == ';':
                        panel_texto.insert(tk.END, "Fin de la línea detectado.\n")
                        break

                    if not token_encontrado:
                        panel_texto.insert(tk.END, f"ERROR: El token '{token}' no corresponde a ninguna categoría conocida (Línea {count})\n")
                        errores.append(f"ERROR: El token '{token}' no corresponde a ninguna categoría conocida (Línea {count})\n")

                panel_texto.insert(tk.END, "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _\n")

            if not (inicio_programa_encontrado and fin_programa_encontrado):
                errores.append(f"Falta marca de inicio o fin del programa (##) en línea {count}.")
            if not (inicio_cuerpo_encontrado and fin_cuerpo_encontrado):
                errores.append(f"Falta marca de inicio o fin del cuerpo del programa (||) en línea {count}.")

            if errores:
                messagebox.showerror("Errores encontrados", "\n".join(errores))
            else:
                messagebox.showinfo("Análisis completado", "El archivo ha sido analizado sin errores detectados.")

# Definiciones de operadores, símbolos de puntuación, variables y palabras reservadas
operadores = {'+': 'Operador de suma', '-': 'Operador de resta', '/': 'Operador de división',
              '^': 'Operador de potencia', '%': 'Operador de módulo', '!=': 'Operador de desigualdad',
              '=': 'Operador de asignación', '<=': 'Operador menor o igual que',
              '>=': 'Operador mayor o igual que', '<': 'Operador menor que',
              '>': 'Operador mayor que', '&': 'AND lógico', '|': 'OR lógico'}
claves_operadores = operadores.keys()

simbolos = {'¡': 'Exclamación invertida', '¿': 'Interrogación invertida',
                       '?': 'Signo de interrogación', '“': 'Comillas', ',': 'Coma',
                       '#': 'Numeral', '$': 'Símbolo de dólar', '%': 'Porcentaje', '&': 'Ampersand',
                       '|': 'Barra vertical', '(': 'Paréntesis que abre', ')': 'Paréntesis que cierra',
                       '{': 'Llave que abre', '}': 'Llave que cierra',
                       '[': 'Corchete que abre', ']': 'Corchete que cierra', ';': 'Punto y coma'}
claves_simbolos = simbolos.keys()

variables = {'Num': 'número entero', 'Real': 'número real',
             'Lett': 'carácter', 'Tram': 'texto o string',
             'List': 'array'}
claves_variables = variables.keys()

palabras_reservadas = {'EscribeEsto': 'Método de escritura',
                       'LeeEsto': 'Método de lectura'}
claves_palabras_reservadas = palabras_reservadas.keys()

def mostrar_info():
    messagebox.showinfo("Información", "Nada puede malir sal...")

ventana = tk.Tk()
ventana.title("Analizador léxico ZeaS")
ventana.geometry("800x600")  # Tamaño de la ventana

# Frame principal
frame_principal = tk.Frame(ventana)
frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

# Botón abrir archivo
boton = tk.Button(frame_principal, text="Abrir archivo", command=procesar_archivo, bg="#4CAF50", fg="white")
boton.pack(pady=10)

# Área de texto
panel_texto = scrolledtext.ScrolledText(frame_principal, wrap=tk.WORD, width=60, height=20)
panel_texto.pack(fill="both", expand=True, padx=10, pady=10)

# Menu
menu_bar = tk.Menu(ventana)
ventana.config(menu=menu_bar)


# Btn ayuda
menu_ayuda = tk.Menu(menu_bar, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=mostrar_info)
menu_bar.add_cascade(label="Firma", menu=menu_ayuda)

# Barra de estado
barra_estado = tk.Label(ventana, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

#Iniciar ventana
ventana.mainloop()
