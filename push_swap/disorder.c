/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   disorder.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 18:19:35 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 19:18:51 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

double compute_disorder(int *arr, int size)
{
    int i, j;
    double mistakes = 0;
    double total_pairs = 0;

    if (size <= 1)
        return (0);
    for (i = 0; i < size - 1; i++)
    {
        for (j = i + 1; j < size; j++)
        {
            total_pairs++;
            if (arr[i] > arr[j])
                mistakes++;
        }
    }
    return (mistakes / total_pairs);
}
