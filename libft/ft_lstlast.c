/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 14:01:47 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/30 14:09:34 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstlast(t_list *lst)
{
	if (!lst)
		return (NULL);
	while (lst->next)
		lst = lst->next;
	return (lst);
}

// int	main(void)
// {
// 	t_list	*head;
// 	t_list	*last_node;

// 	head = NULL;
// 	ft_lstadd_front(&head, ft_lstnew("Node 1"));
// 	ft_lstadd_front(&head, ft_lstnew("Node 2"));
// 	ft_lstadd_front(&head, ft_lstnew("Node 3"));
// 	last_node = ft_lstlast(head);
// 	if (last_node)
// 		printf("The last node contains: %s\n", (char *)last_node->content);
// 	else
// 		printf("The list is empty.\n");
// 	return (0);
// }
