"use client";

import { useEffect, useState } from 'react';
import { apiPost, apiGet } from '@/utils/api';
import CreateQuestion from '@/components/CreateQuestion';

interface PageProps {
  params: {
    name: string;
  };
}

export default function Page({ params }: PageProps) {
  const { name } = params;

  const [subject, setSubject] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet(`subjects/?name=${name}`)
    .then(result => {
      if (result.length === 0)  {
        alert("Você está acessando uma página não existente")
        return;
      }

      setSubject(result[0].id);
      setLoading(false);
    })
  }, [name])


  if (loading || subject === null) {
    return (
      <div>loading...</div>
    )
  }

  return (
    <div>
      <CreateQuestion subjId={subject} createQuestionCallback={() => alert("Questão criada com sucesso")} />
    </div>
  )
}
