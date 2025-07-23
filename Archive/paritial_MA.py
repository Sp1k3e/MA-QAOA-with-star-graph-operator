def build_MA_qaoa_ansatz(graph, parameter_list, no_layers, pauli_dict, mode, initial_state = []):
    no_edges = graph.number_of_edges() 
    no_qubits = graph.number_of_nodes() 
    if len(initial_state) == 0:
        dens_mat = initial_density_matrix(no_qubits)
    else:
        dens_mat = qi.DensityMatrix(initial_state)
        dens_mat = sparse.csr_matrix(dens_mat.data)

    #! 只改Mixer
    if(mode == 'M'):
        ham_parameters = parameter_list[:no_layers]
        mixer_parameters = parameter_list[no_layers:]

        # every layer
        for layer in range(no_layers):
            cut_unit = cut_unitary(graph, ham_parameters[layer], pauli_dict)
            dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

            first = True
            for i in range(no_qubits):
                if first:
                    mix_unit = mixer_unitary('X' + str(i), mixer_parameters[i + no_qubits * layer], pauli_dict, no_qubits)
                    first = False
                else:
                    mix_unit = mix_unit * mixer_unitary('X' + str(i), mixer_parameters[i + no_qubits * layer], pauli_dict, no_qubits)

            dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    elif(mode == 'SM'):
        ham_parameters = parameter_list[:no_layers]
        mixer_parameters = parameter_list[no_layers:]

        # every layer
        for layer in range(no_layers - 1):
            cut_unit = cut_unitary(graph, ham_parameters[layer], pauli_dict)
            dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

            mix_unit = mixer_unitary('standard_x', mixer_parameters[layer], pauli_dict, no_qubits)

            dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

        cut_unit = cut_unitary(graph, ham_parameters[no_layers - 1], pauli_dict)
        dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

        first = True
        for i in range(no_qubits):
            if first:
                mix_unit = mixer_unitary('X' + str(i), mixer_parameters[i + no_layers - 1], pauli_dict, no_qubits)
                first = False
            else:
                mix_unit = mix_unit * mixer_unitary('X' + str(i), mixer_parameters[i + no_layers - 1], pauli_dict, no_qubits)

        dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    #! 只改Phaser
    elif(mode == "P"):
        ham_parameters = parameter_list[:no_layers * no_edges]
        mixer_parameters = parameter_list[no_layers * no_edges:]

        for layer in range(no_layers):
            cut_unit = MA_cut_unitary(graph, ham_parameters[layer * no_edges: (layer + 1) * no_edges], pauli_dict)
            dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

            mix_unit = mixer_unitary('standard_x', mixer_parameters[layer], pauli_dict, no_qubits)
            dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    #! 都改
    elif(mode == "All"):
        ham_parameters = parameter_list[:no_layers * no_edges]
        mixer_parameters = parameter_list[no_layers * no_edges:]

        for layer in range(no_layers):
            cut_unit = MA_cut_unitary(graph, ham_parameters[layer * no_edges: (layer + 1) * no_edges], pauli_dict)
            dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

            first = True
            for i in range(no_qubits):
                if first:
                    mix_unit = mixer_unitary('X' + str(i), mixer_parameters[i + no_qubits * layer], pauli_dict, no_qubits)
                    first = False
                else:
                    mix_unit = mix_unit * mixer_unitary('X' + str(i), mixer_parameters[i + no_qubits * layer], pauli_dict, no_qubits)

            dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    return dens_mat